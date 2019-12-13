import asyncio
import itertools
import logging
import threading

# pylint: disable=invalid-name
# pylint: disable=global-statement
try:
    # Python 3.8 or newer has a suitable process watcher
    asyncio.ThreadedChildWatcher
except AttributeError:
    # backport the Python 3.8 threaded child watcher
    import os
    import warnings

    # Python 3.7 preferred API
    _get_running_loop = getattr(asyncio, "get_running_loop", asyncio.get_event_loop)

    class _Py38ThreadedChildWatcher(asyncio.AbstractChildWatcher):
        def __init__(self):
            self._pid_counter = itertools.count(0)
            self._threads = {}

        def is_active(self):
            return True

        def close(self):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def __del__(self, _warn=warnings.warn):
            threads = [t for t in list(self._threads.values()) if t.is_alive()]
            if threads:
                _warn(
                    f"{self.__class__} has registered but not finished child processes",
                    ResourceWarning,
                    source=self,
                )

        def add_child_handler(self, pid, callback, *args):
            loop = _get_running_loop()
            thread = threading.Thread(
                target=self._do_waitpid,
                name=f"waitpid-{next(self._pid_counter)}",
                args=(loop, pid, callback, args),
                daemon=True,
            )
            self._threads[pid] = thread
            thread.start()

        def remove_child_handler(self, pid):
            # asyncio never calls remove_child_handler() !!!
            # The method is no-op but is implemented because
            # abstract base class requires it
            return True

        def attach_loop(self, loop):
            pass

        def _do_waitpid(self, loop, expected_pid, callback, args):
            assert expected_pid > 0

            try:
                pid, status = os.waitpid(expected_pid, 0)
            except ChildProcessError:
                # The child process is already reaped
                # (may happen if waitpid() is called elsewhere).
                pid = expected_pid
                returncode = 255
                logger.warning(
                    "Unknown child process pid %d, will report returncode 255", pid
                )
            else:
                if os.WIFSIGNALED(status):
                    returncode = -os.WTERMSIG(status)
                elif os.WIFEXITED(status):
                    returncode = os.WEXITSTATUS(status)
                else:
                    returncode = status

                if loop.get_debug():
                    logger.debug(
                        "process %s exited with returncode %s", expected_pid, returncode
                    )

            if loop.is_closed():
                logger.warning("Loop %r that handles pid %r is closed", loop, pid)
            else:
                loop.call_soon_threadsafe(callback, pid, returncode, *args)

            self._threads.pop(expected_pid)

    # add the watcher to the loop policy
    asyncio.get_event_loop_policy().set_child_watcher(_Py38ThreadedChildWatcher())

__all__ = ["EventLoopThread", "get_event_loop", "stop_event_loop", "run_coroutine"]

logger = logging.getLogger(__name__)


class EventLoopThread(threading.Thread):
    loop = None
    _count = itertools.count(0)

    def __init__(self):
        name = f"{type(self).__name__}-{next(self._count)}"
        super().__init__(name=name, daemon=True)

    def __repr__(self):
        loop, r, c, d = self.loop, False, True, False
        if loop is not None:
            r, c, d = loop.is_running(), loop.is_closed(), loop.get_debug()
        return (
            f"<{type(self).__name__} {self.name} id={self.ident} "
            f"running={r} closed={c} debug={d}>"
        )

    def run(self):
        self.loop = loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            loop.run_forever()
        finally:
            try:
                shutdown_asyncgens = loop.shutdown_asyncgens()
            except AttributeError:
                pass
            else:
                loop.run_until_complete(shutdown_asyncgens)
            loop.close()
            asyncio.set_event_loop(None)

    def stop(self):
        loop, self.loop = self.loop, None
        if loop is None:
            return
        loop.call_soon_threadsafe(loop.stop)
        self.join()


_lock = threading.Lock()
_loop_thread = None


def get_event_loop():
    global _loop_thread
    with _lock:
        if _loop_thread is None:
            _loop_thread = EventLoopThread()
            _loop_thread.start()
        return _loop_thread.loop


def stop_event_loop():
    global _loop_thread
    with _lock:
        if _loop_thread is not None:
            _loop_thread.stop()
            _loop_thread = None


def run_coroutine(coro):
    return asyncio.run_coroutine_threadsafe(coro, get_event_loop())
