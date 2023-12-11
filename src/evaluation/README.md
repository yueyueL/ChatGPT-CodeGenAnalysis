# Static analysi for ChatGPT-generated code

This readme provides information on how to download, install, and use Pylint, flake8, pycodestyle, and PMD to analyze Python and Java code.

## Python Code Analysis
### Pylint
Pylint is a Python static code analysis tool that checks for programming errors, enforces coding standards, and provides recommendations for code improvements.

#### Installation
Install Pylint using pip:
```
pip install pylint
```

#### Usage
To analyze a Python file using Pylint, run the following command:
```
pylint <file_name>.py
```

### Flake8
flake8 is a Python linting tool that combines pycodestyle, PyFlakes, and McCabe complexity checks.

#### Installation
Install flake8 using pip:
```
pip install flake8
```
#### Usage
To analyze a Python file using flake8, run the following command:
```
flake8 <file_name>.py
```

## Java Code Analysis
### PMD
PMD is an extensible cross-language static code analyzer that supports Java, JavaScript, Salesforce.com Apex, PL/SQL, Apache Velocity, XML, XSL, and more.

#### Installation
1. Download the latest PMD release from the [official website](https://pmd.github.io/).
2. Extract the downloaded archive to a folder of your choice.
3. Add the `bin` folder inside the extracted directory to your system's `PATH` environment variable.

#### Usage
To analyze a Java file using PMD, run the following command:
```
pmd check -d <file_name>.java -R <ruleset_file>.xml
```
where `<ruleset_file>` is the name of the ruleset file to use for the analysis. The `rulesets` folder in this repository contains the ruleset files used for the experiments in the paper.

In our analysis, we used the following rulesets: `rulesets-pmd/java/all.xml`


### CheckStyle
CheckStyle is a static code analysis tool that checks Java code for adherence to a configurable coding standard.

#### Usage
To analyze a Java file using CheckStyle, run the following command:
```
java -jar checkstyle/checkstyle-10.9.3-all.jar -c checkstyle/sun_checks.xml <file_name>.java
```


## Running the Analysis by script
To run the analysis on a set of files, use the `analysis_by_command.py` script. 

