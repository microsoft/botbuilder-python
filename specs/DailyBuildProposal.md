# Daily Build Propsal for .Net BotBuilder SDK

This proposal describes our plan to publish daily builds for consumption. The goals of this are:
1. Make it easy for developers (1P and 3P) to consume our daily builds.
2. Exercise our release process frequently, so issues don't arise at critical times.
3. Meet Developers where they are.

Use the [ASP.Net Team](https://github.com/dotnet/aspnetcore/blob/master/docs/DailyBuilds.md) as inspiration, and draft off the work they do.

# Versioning
Move to Python suggested versioning for dailies defined in [PEP440](https://www.python.org/dev/peps/pep-0440/#developmental-releases).

The tags we use for preview versions are:
```
.<yyyymmdd>.dev{incrementing value}
-rc{incrementing value}
```

# Daily Builds
All our Python wheel packages would be pushed to the SDK_Public project at [fuselabs.visualstudio.com](https://fuselabs.visualstudio.com).

    Note: Only a public project on Devops can have a public feed. The public project on our Enterprise Tenant is [SDK_Public](https://fuselabs.visualstudio.com/SDK_Public).

This means developers could add this feed their projects by adding the following command on a pip conf file, or in the pip command itself:

```bash
extra-index-url=https://pkgs.dev.azure.com/ConversationalAI/BotFramework/_packaging/SDK%40Local/pypi/simple/
```

## Debugging
To debug daily builds in VSCode:
* In the launch.json configuration file set the option `"justMyCode": false`.

## Daily Build Lifecyle
Daily builds older than 90 days are automatically deleted.

# Summary - Weekly Builds
Once per week, preferably on a Monday, a daily build is pushed to PyPI test. This build happens from 'main', the same as a standard daily build. This serves 2 purposes:

1. Keeps PyPI "Fresh" for people that don't want daily builds.
2. Keeps the release pipelines active and working, and prevents issues.

These builds will have the "-dev" tag and ARE the the daily build.

**This release pipeline should be the EXACT same pipeline that releases our production bits.**

Weekly builds older than 1 year should be automatically delisted.

## Adding packages to the feed
Our existing Release pipelines would add packages to the feed.
# Migration from MyGet

1. Initially, our daily builds should go to both MyGet and Azure Devops.
2. Our docs are updated once builds are in both locations.
3. Towards the end of 2020, we stop publising to MyGet.

# Containers
ASP.Net and .Net Core 5 also publish a container to [Docker Hub](https://hub.docker.com/_/microsoft-dotnet-nightly-aspnet/) as part of their daily feed. We should consider that, along with our samples, in the next iteration of this work.
