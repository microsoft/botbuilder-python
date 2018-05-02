'use strict';
const Generator = require('yeoman-generator');
const chalk = require('chalk');
const yosay = require('yosay');
const path = require('path');
const _ = require('lodash');
const mkdirp = require('mkdirp');

module.exports = class extends Generator {
  prompting() {
    // Have Yeoman greet the user.
    this.log(
      yosay(`Welcome to the laudable ${chalk.red('generator-botbuilder-python')} generator!`)
    );

    const prompts = [
      { name: 'botName', message: `What 's the name of your bot?`, default: 'sample' },
      { name: 'description', message: 'What will your bot do?', default: 'sample' },
      { name: 'dialog', type: 'list', message: 'Which default dialog do you want?', choices: ['Echo'] },
    ];

    return this.prompt(prompts).then(props => {
      // To access props later use this.props.someAnswer;
      this.props = props;
    });
  }

  writing() {
    const directoryName = _.kebabCase(this.props.botName);

    if (path.basename(this.destinationPath()) !== directoryName) {
      this.log(`Your bot should be in a directory named ${ directoryName }\nI'll automatically create this folder.`);
      mkdirp(directoryName);
      this.destinationRoot(this.destinationPath(directoryName));
    }

    this.fs.copyTpl(this.templatePath('requirements.txt'), this.destinationPath('requirements.txt'), { botName: directoryName });
    this.fs.copy(this.templatePath(`main.py`), this.destinationPath(`main.py`));
    this.fs.copyTpl(this.templatePath('README.md'), this.destinationPath('README.md'), {
      botName: this.props.botName, description: this.props.description
    });
  }

  install() {
    this.installDependencies({ bower: false });
  }
};
