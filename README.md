<h1 align="center">
    <a href="https://github.com/BrenoFariasdaSilva/Worked-Example-Miner">Worked-Example-Miner</a>
    <img src="https://github.com/BrenoFariasdaSilva/Worked-Example-Miner/blob/main/.assets/Icons/Bash.svg" width="30" height="30">
</h1>

<div align="center">
  
---

Welcome to my Worked-Example-Miner Repository!

The [Worked-Example-Miner](https://github.com/BrenoFariasdaSilva/Worked-Example-Miner) is a comprehensive tool for Java repository analysis. This tool integrates [AutoMetric](https://github.com/BrenoFariasdaSilva/AutoMetric), [CK](https://github.com/mauricioaniche/ck), [Google Gemini API](https://ai.google.dev/), [PyDriller](https://github.com/ishepard/pydriller), and [RefactoringMiner](https://github.com/tsantalis/RefactoringMiner) to analyze Java repositories and generate data and metadata on the software's design evolution and quality. The tool is designed to identify trends in how repositories evolve over time and select prime candidates for creating worked examples.

This project is massive and complex, containing multiple integrated tools and exploring different goals and research questions. With that in mind, each of the directories in this repository has its own `README.md` file explaining it's purpose and how it contributes to the overall project. 

---

</div>

<div align="center">

![GitHub Build/WorkFlow](https://img.shields.io/github/actions/workflow/status/BrenoFariasDaSilva/Scientific-Research/update-worked-example-miner-submodule.yml)
![AutoMetric SubModule](https://img.shields.io/github/actions/workflow/status/BrenoFariasdaSilva/Worked-Example-Miner/update-autometric-submodule.yml?label=AutoMetric%20SubModule)
![CK SubModule](https://img.shields.io/github/actions/workflow/status/BrenoFariasdaSilva/Worked-Example-Miner/update-ck-submodule.yml?label=CK%20SubModule)
![GitHub Code Size in Bytes](https://img.shields.io/github/languages/code-size/BrenoFariasdaSilva/Worked-Example-Miner)
![GitHub Commits](https://img.shields.io/github/commit-activity/t/BrenoFariasDaSilva/Worked-Example-Miner/main)
![GitHub Last Commit](https://img.shields.io/github/last-commit/BrenoFariasdaSilva/Worked-Example-Miner)
![GitHub Forks](https://img.shields.io/github/forks/BrenoFariasDaSilva/Worked-Example-Miner)
![GitHub Language Count](https://img.shields.io/github/languages/count/BrenoFariasDaSilva/Worked-Example-Miner)
![GitHub License](https://img.shields.io/github/license/BrenoFariasdaSilva/Worked-Example-Miner)
![GitHub Stars](https://img.shields.io/github/stars/BrenoFariasdaSilva/Worked-Example-Miner)
![wakatime](https://wakatime.com/badge/github/BrenoFariasdaSilva/Worked-Example-Miner.svg)

</div>

<div align="center">
   
![Repobeats Statistics](https://repobeats.axiom.co/api/embed/cc926b338fcd1c49112ae0c1707e41cbfc07f606.svg "Repobeats analytics image")

</div>

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Setup](#setup)
  - [Clone with Submodules](#clone-with-submodules)
  - [Clone without Submodules (Not Recommended)](#clone-without-submodules-not-recommended)
  - [Clone Submodules](#clone-submodules)
  - [Python and Pip](#python-and-pip)
    - [Linux](#linux)
    - [MacOS](#macos)
    - [Windows](#windows)
  - [Additional Requirements](#additional-requirements)
    - [Git](#git)
      - [Linux](#linux-1)
      - [MacOS](#macos-1)
      - [Windows](#windows-1)
    - [Make](#make)
      - [Linux](#linux-2)
      - [MacOS](#macos-2)
      - [Windows](#windows-2)
    - [Apache Maven](#apache-maven)
      - [Linux](#linux-3)
      - [MacOS](#macos-3)
      - [Windows](#windows-3)
- [Paper Submissions](#paper-submissions)
  - [EduComp 2024 - Ideas Laboratory](#educomp-2024---ideas-laboratory)
- [Goals](#goals)
- [Skills](#skills)
- [Directories](#directories)
- [Repositories](#repositories)
  - [Apache Kafka](#apache-kafka)
  - [Apache ZooKeeper](#apache-zookeeper)
- [Methodology](#methodology)
  - [Data Collection](#data-collection)
  - [Code Analysis](#code-analysis)
- [Research Questions](#research-questions)
- [Proposed Approach](#proposed-approach)
  - [Software Metrics](#software-metrics)
  - [Refactorings Patterns](#refactorings-patterns)
  - [Tools Utilized](#tools-utilized)
- [Conclusion](#conclusion)
- [How to Cite?](#how-to-cite)
- [Contributing](#contributing)
- [Collaborators](#collaborators)
- [License](#license)

## Introduction

The [Worked-Example-Miner](https://github.com/BrenoFariasdaSilva/Worked-Example-Miner) project is a comprehensive research endeavor that delves into the evolution of code in Java repositories, focusing on Distributed Systems (DS). By integrating specialized tools and metrics, we aim to analyze code quality, identify patterns of improvement, and select exemplary code segments for educational purposes. Our research explores the intricacies of software engineering, emphasizing the importance of code metrics, refactoring, and code evolution in enhancing software design quality and maintainability

Within this repository, you'll find a wealth of resources, from detailed code analyses and data sets to insightful findings and theoretical advancements. Whether you're a researcher seeking to deepen your understanding of software evolution, a developer looking for proven practices in distributed systems, or an educator aiming to enrich your curriculum, this documentation offers valuable knowledge and tools to support your goals.

## Setup

This section provides instructions for installing the Python Language and Pip Python package manager and the project's requirements, such as `make` and `mvn`.

### Clone with Submodules

In order to clone this repository with the submodules (AutoMetric and CK), you can use the following command:

```bash
git clone --recurse-submodules https://github.com/BrenoFariasdaSilva/Worked-Example-Miner.git
```

### Clone without Submodules (Not Recommended)

In order to clone this repository without the submodules (AutoMetric and CK), you can use the following command:

```bash
git clone https://github.com/BrenoFariasdaSilva/Worked-Example-Miner
```

### Clone Submodules

In case you have already cloned the repository and forgot to clone the submodules (AutoMetric and CK), you can use the following command to clone the submodule:

```bash
git submodule init
git submodule update
```

### Python and Pip

In order to run the scripts, you must have python3 and pip installed in your machine. If you don't have it installed, you can use the following commands to install it:

#### Linux

In order to install python3 and pip in Linux, you can use the following commands:

```
sudo apt install python3 -y
sudo apt install python3-pip -y
```

#### MacOS

In order to install python3 and pip in MacOS, you can use the following commands:

```
brew install python3
```

#### Windows

In order to install python3 and pip in Windows, you can use the following commands in case you have `choco` installed:

```
choco install python3
```

Or just download the installer from the [official website](https://www.python.org/downloads/).

Great, you now have python3 and pip installed. Now, we need to install the additional project requirements.

### Additional Requirements

In addition to Python and Pip, you will need to install some other tools to successfully run the project. These tools include `git`, `make` and `mvn` (Apache Maven).

#### Git

`git` is a distributed version control system that is widely used for tracking changes in source code during software development. In this project, `git` is used to download and manage the analyzed repositories, as well as to clone the project and its submodules. To install `git`, follow the instructions below based on your operating system:

##### Linux

To install `git` on Linux, run:

```bash
sudo apt install git -y
```

##### MacOS

To install `git` on MacOS, you can use Homebrew:

```bash
brew install git
```

##### Windows

On Windows, you can download `git` from the official website [here](https://git-scm.com/downloads) and follow the installation instructions provided there.

#### Make

`make` is a build automation tool that is commonly used to manage and maintain projects. In this project, `make` is used to automate the execution of tasks, such as running scripts and managing python/pip dependencies. To install `make`, you can use the following commands based on your operating system:

##### Linux
To install `make` on Linux, run:

```bash
sudo apt install make -y
```

##### MacOS
To install `make` on MacOS, you can install it via Homebrew:

```bash
brew install make
```

##### Windows
On Windows, you can install `make` as part of a Unix-like environment such as Cygwin or WSL (Windows Subsystem for Linux). If you are using WSL, you can follow the Linux instructions above.

Or you can download it manually from the official GNU Make website [here](https://www.gnu.org/software/make/#download) and follow the installation instructions provided there.

#### Apache Maven

Apache Maven is a project management tool that is primarily used for Java projects. In this project, Maven is used to manage dependencies and build the CK Java project JAR file, which is used to extract code metrics from Java repositories. It helps manage project dependencies and build processes. To install Maven, follow these instructions based on your operating system:

##### Linux
To install Maven on Linux, use:

```bash
sudo apt install maven -y
```

##### MacOS
To install Maven on MacOS, use Homebrew:

```bash
brew install maven
```

##### Windows
On Windows, you can use Chocolatey to install Maven:

```bash
choco install maven
```

Or you can download it manually from the official Maven website [here](https://maven.apache.org/download.cgi) and follow the installation instructions provided there.

## Paper Submissions

This research project aims to contribute to the field of Software Engineering (SE) and Distributed Systems (DS) by exploring the evolution of code quality in Java repositories. Our research findings and insights will be shared through academic papers, conference presentations, and educational resources. We are committed to advancing knowledge in software development practices and improve the educational quality of worked examples in SE.

### EduComp 2024 - Ideas Laboratory

We are excited to announce that our paper's submission to the [EduComp 2024](http://educompbrasil.org) conference was accepted! EduComp is a premier conference that focuses on educational computing, providing a platform for researchers, educators, and practitioners to share their insights and innovations in the field of educational technology. Our paper highlights the significance of worked examples in software engineering education, particularly within the domain of Distributed Systems, and discusses a novel approach for selecting these examples based on code quality metrics.

The study introduces a heuristic based on metrics to examine the evolution of code quality in Distributed Systems, aiming to identify code examples that demonstrate significant improvements. Using software projects such as Apache Kafka and ZooKeeper, the research applies tools like CK (Java code metrics calculator) and RefactoringMiner integrated into the developed Worked Example Miner (WEM) tool. This approach allowed for the generation of statistical descriptions, linear regressions, and refactorings that aid in selecting code changes for worked examples.

Our findings reveal that this methodology can effectively contribute to the selection of worked examples for Distributed Systems, highlighting improvements in modularization, cohesion, and code reusability. Such examples are instrumental in enhancing learning and understanding in software engineering education.

For further details on our approach and findings, you can read our paper submission here: [Abordagem para seleção de exemplos trabalhados para Engenharia de Software do domínio de Sistemas Distribuídos](https://sol.sbc.org.br/index.php/educomp_estendido/article/view/29466) and watch our presentation at EduComp 2024 on April 25 available on [YouTube](https://youtu.be/g_5z_1xqKKU?si=L2e6s5mQ2xs-w9aZ).

EduComp24, April 22-27, 2024, São Paulo, São Paulo, Brazil (Online)

© 2024 Copyright maintained by the authors. Publication rights licensed to the Brazilian Computer Society (SBC).

<!-- ### SIGCSE 2025 (UPDATE)

We are also planning to submit a paper to the [SBES 2024](https://cbsoft.sbc.org.br/2024/sbes/) conference. SBES is the Brazilian Symposium on Software Engineering, a prestigious event that brings together researchers, practitioners, and students to discuss the latest trends and advancements in software engineering. Our paper will delve into the evolution of code quality metrics in Java repositories, focusing on Distributed Systems (DS) and the implications for software design and maintainability. You can our paper submission here [Abordagem para seleção de exemplos trabalhados para Engenharia de Software do domínio de Sistemas Distribuídos](UPDATE). -->

## Goals

1. **Code Metrics Generation:**
   - Traverse the repository commit history using PyDriller.
   - Extract code metrics using CK (Chidamber & Kemerer) metrics for Java repositories.
   - Extract refactoring patterns using RefactoringMiner for Java repositories.

2. **Code Metrics Selection:**
   - Identify relevant code quality metrics for analyzing Distributed Systems (DS) evolution.
   - Evaluate the significance of selected metrics in reflecting code quality improvements.
   - Analyze the correlation between code quality metrics and non-functional characteristics.

3. **Analyzing Code Evolution:**
   - Analyze code that started with "bad" values for the select metrics and evolved over time.
   - Identify good code examples that indicate what makes code better and what changes are typically made to improve it.

4. **Educational Code Examples:**
    - Develop a heuristic for selecting code examples that represent quality improvements in DS.
    - Identify code segments that demonstrate effective practices for code improvement.
    - Create worked examples that highlight the adaptation and evolution of DS code over time.

## Skills

Our research project involves expertise in the following areas:

- Python Language.
- Python Libraries (Pandas, Matplotlib, NumPy, Scikit-Learn).
- Java Language.
- CK (Chidamber & Kemerer) Metrics.
- PyDriller.
- RefactoringMiner (Refactoring Detection).
- Software Engineering.
- Distributed Systems.
- Worked Examples.
- Statistical Data Analysis and Visualization (Min, Max, Average, Third Quartile, Median, Linear Regression).
- Apache Kafka (Distributed Messaging System).
- Apache ZooKeeper (Distributed Coordination Service).
- GitHub Repositories.
- Data Collection and Analysis.
- Makefile.
- Virtual Environment.

Feel free to explore the code and data in this repository. If you have any questions or suggestions, please don't hesitate to reach out to me.

## Directories

Each directory in this repository has its own README.md file explaining its purpose. Please refer to individual README files for more details.

- **PyDriller:** This Python library excels in mining software repositories. Within Worked Example Miner, PyDriller is harnessed to navigate through the commit tree of a repository, facilitating the execution of CK at every commit, thereby ensuring a comprehensive analysis across the development timeline.
This directory will contains two main files: `code_metrics.py` and `metrics_changes.py`. The `code_metrics.py` file is responsible for extracting the CK metrics from the Java repositories, as well as generating commit diff files and a commit hashes list file. In the other hand, the `metrics_changes.py` file is responsible for reading the generated ck metrics files and generate the metrics statistics, linear regressions, detecting substantial changes, and identifying refactoring types.

- **RefactoringMiner:** This directory contains the RefactoringMiner tool, which specializes in detecting refactorings in Java repositories. By integrating RefactoringMiner into Worked Example Miner, we can identify and analyze refactorings that contribute to code evolution, highlighting changes that enhance code quality and maintainability. This directory will contains two main files: `metrics_evolution_refactorings.py` and `repositories_refactorings.py`. The `metrics_evolution_refactorings.py` file is responsible for generating the refactorings files for the selected files in the Java repositories. The `repositories_refactorings.py` file is responsible for generating the refactorings file for the selected repositories in the Java repositories.

- **Gemini:** This directory contains the `gemini.py` python code that interacts with the Google Gemini API. By integrating Gemini into Worked Example Miner, we can give some of the data and metadata generated by the CK tool and RefactoringMiner to the Google Gemini API in order to analyze, for example, if the given examples refined by our heuristic are good examples for educational purposes. Actually, this integration makes this a general purpose analysis tool, as the data and metadata generated by CK is only restricted by Java repositories, the analysis generated by Gemini only depends on the existance of the data and metadata generated by PyDriller (integrates CK) and/or RefactoringMiner. So, in order to expand the analysis of Gemini to other contexts other than Distributed Systems, all you need to do is change the context given in the `start_context` variable in the `Gemini/gemini.py` file.

By leveraging the combined strengths of these tools, Worked Example Miner emerges as a powerhouse for Java repository analysis. It not only facilitates the generation of differential analyses for each commit but also meticulously tracks the historical progression of selected CK metrics at each stage of code development. Furthermore, the tool is equipped to conduct linear regression analyses, detect substantial changes, and identify refactoring types cataloged by RefactoringMiner.

The integration of these capabilities allows Worked Example Miner to produce an array of outputs, from detailed commit diffs to analyses of repository evolution and potential trends. Such comprehensive data is instrumental in pinpointing exemplary candidates for the creation of worked examples, thus enriching educational resources and facilitating a deeper understanding of Java repository dynamics.

In essence, Worked Example Miner stands as a testament to the synergy of combining specialized tools to achieve a greater understanding of software development practices by the code metrics evolution. Through its detailed analyses, educators, researchers, and developers are better equipped to study Java repositories, enabling the cultivation of rich, informative worked examples that highlight best practices and evolutionary insights in software development.

## Repositories

Our research project focuses on analyzing the evolution of code in Java repositories, with a particular emphasis on Distributed Systems (DS). We have selected two prominent repositories, Apache Kafka and Apache ZooKeeper, to serve as case studies for our investigation. These repositories are renowned for their contributions to distributed messaging systems and coordination services, respectively, making them ideal candidates for studying code evolution in DS. Also, they are widely used in the industry and academia, are open-source, and are still actively maintained and developed.

### [Apache Kafka](https://github.com/apache/kafka)

- **Purpose:** Apache Kafka is a distributed messaging system based on the publish-subscribe model, widely used for building real-time data processing infrastructures. It is designed to handle large-scale data flows, enabling organizations to process, store, and transmit data efficiently.
- **Usage in Research:** Kafka's architecture, real-world usage, and capability to handle massive volumes of real-time data make it an excellent candidate for our study. It provides insights into the design and maintenance of distributed systems and how they evolve to meet scalability, fault tolerance, and data distribution requirements.

### [Apache ZooKeeper](https://github.com/apache/zookeeper)

- **Purpose:** Apache ZooKeeper is a distributed coordination service widely used for large-scale internet systems. It offers a reliable and highly available environment for coordinating tasks across multiple nodes in a distributed cluster.
- **Usage in Research:** ZooKeeper's role in providing a consensus service for distributed systems and its mechanisms for ensuring data consistency across nodes makes it invaluable for studying distributed service coordination, management, and the evolution of critical infrastructure components in distributed systems.

This are the main repositories that we are analyzing in this research project, but for future work, we can expand the analysis to other repositories in order to consolidade our methodology and improve the results.

## Methodology

This research adopts a systematic approach to explore the evolution of Distributed Systems (DS) through code metric analysis. Our methodology encompasses data collection, code analysis, and the integration of several tools and metrics to examine how code evolves in terms of complexity, quality, efficiency and in many other aspects.

### Data Collection

- **Repositories Selection:** We select relevant repositories that align with our research goals, focusing on projects like Apache Kafka and ZooKeeper.
- **CK Integration:** CK tool is integrated for conducting code metric analysis on chosen commits, classes, or methods within the repositories.
- **Mining Software Repositories:** PyDriller is utilized to navigate through the commit history, extracting essential data regarding code metrics and their evolution.
- **Metric Evaluation:** We evaluate code metrics that generates the values of each selected metric for each state (commit) of the code. This allows us to identify trends, patterns, and changes in the code over time.
- **Metric Visualization:** We employ Matplotlib for generating visual representations that illustrate the progression of code metrics over time.
- **RefactoringMiner Integration:** RefactoringMiner is used to detect refactorings in the codebase that signal improvements or changes contributing to code evolution.

### Code Analysis

We analyze instances where code initially demonstrated suboptimal metrics but evolved positively over time. Identifying exemplary modifications sheds light on effective practices for code improvement, focusing on alterations that enhance metric scores.

## Research Questions

Our investigation is guided by four principal questions:

1. How to identify relevant code quality metrics for analyzing DS evolution?
2. What patterns and trends signify clear code improvement in DS?
3. How do code improvements reflect on selected metrics and their correlation with non-functional characteristics?
4. Which metrics and characteristics are crucial for selecting appropriate code examples for educational purposes in Software Engineering (SE)?

## Proposed Approach

The project aims to develop a heuristic for identifying code examples that represent quality improvements in DS. This heuristic will aid in selecting code segments for educational examples, illustrating the adaptation and evolution of DS code over time. The heuristic will focus on improvements detectable through selected metrics, using specific tools on carefully chosen open-source repositories.

### Software Metrics

Our analysis leverages a suite of metrics for object-oriented design as outlined in the seminal work by Chidamber and Kemerer. The study, titled "A Metrics Suite for Object Oriented Design," was published in the IEEE Transactions on Software Engineering (vol. 20, no. 6, pp. 476–493, 1994). It introduces key metrics that have become foundational in assessing and improving the design quality of object-oriented software systems. These metrics include:

- **Coupling Between Object classes (CBO):** Reflects the degree of coupling by measuring the number of classes directly associated with a given class through method calls. A higher CBO value suggests higher complexity and lower flexibility, potentially leading to increased maintenance challenges. Reducing CBO over time can indicate improvements in code quality, aiming for a more modular software design that minimizes the impact of changes across the system.

- **Response for a Class (RFC):** Represents the set of methods that can be executed in response to a message received by an instance of the class. A lower RFC value denotes fewer behaviors and potentially lower complexity, making the class more cohesive and easier to maintain and test.

- **Weighted Methods per Class (WMC):** Calculates the sum of complexity measures of the class's methods. High WMC values may indicate complex classes with multiple responsibilities, affecting development and maintenance costs. Lower WMC values suggest a more focused and cohesive class, facilitating understanding and extension.

Additionally, the CK tool offers insights into other metrics that help understand code evolution:

- **Depth of Inheritance Tree (DIT):** Measures the number of ancestor classes, indicating the complexity level and the potential for side effects from changes in superclasses. A higher DIT value can imply more complex inheritance structures that may affect maintainability.

- **Lack of Cohesion in Methods (LCOM):** Indicates the degree of method cohesion within a class, ranging from 0 (high cohesion) to 1 (low cohesion). Preferred low values suggest that methods within a class are closely related to each other, enhancing the class's cohesiveness.

- **Number of Children (NOC):** Counts the direct subclasses of a class, with higher values hinting at greater reusability and significance within the codebase, as it implies a foundational role due to other classes' dependency on it.

### Refactorings Patterns

Refactorings play a crucial role in software evolution, enabling developers to enhance code quality, maintainability, and extensibility. By detecting and analyzing refactorings, we can identify patterns of improvement and understand how code evolves to meet changing requirements and design goals. RefactoringMiner is a powerful tool that automates the detection of refactorings in Java repositories, providing valuable insights into code changes and their implications.

Refactorings can be categorized into several types, each serving a specific purpose in code improvement, but these are the ones we use in our research:
- **Extract Method:** Involves extracting a block of code into a new method to improve readability, maintainability, and reusability. This refactoring reduces code duplication and enhances modularity.
- **Extract Class:** Separates part of a class into a new class to enhance cohesion and reduce complexity. This refactoring promotes a more focused and modular design, facilitating future changes and extensions.
- **Extract Superclass:** Creates a superclass to encapsulate common behavior shared by multiple classes, promoting code reuse and modularity. This refactoring simplifies the inheritance hierarchy and enhances maintainability.
- **Pull Up Method:** Moves a method from a subclass to a superclass to promote code reuse and simplify the inheritance hierarchy. This refactoring enhances modularity and reduces duplication.
- **Push Down Method:** Transfers a method from a superclass to a subclass to enhance encapsulation and modularity. This refactoring ensures that methods are located closer to the data they operate on, improving code organization and maintainability and avoiding the "God class" anti-pattern. "God class" is a design flaw where a single class handles most of the system's functionality, breaking the Single Responsibility Principle and leading to poor maintainability and extensibility.

Collectively, these metrics and refactorings provide a comprehensive view of the codebase's complexity, quality, and maintainability. They serve as essential tools for developers to refine software design and architecture effectively. It's important to note that these metrics are derived from static code analysis, which involves evaluating the source code without executing the program. This approach allows for an in-depth understanding of the code's structural and qualitative aspects, facilitating targeted improvements and ensuring a more robust, maintainable, and efficient software system.

Dynamic code analysis complements our understanding by examining the code's behavior during execution. It sheds light on runtime characteristics, class communication, performance, and resource utilization, offering a holistic view of the software's operational efficiency. Despite the value of dynamic analysis, our research emphasizes static code analysis. This focus allows us to delve into the software quality's evolution within the domain of Distributed Systems (DS), providing insights into the code design changes and their impact on maintainability and reliability over time.

### Tools Utilized

- **[CK Tool](https://github.com/mauricioaniche/ck) (with Enhancements):** This repository includes a fork of the original CK tool, tailored for static code analysis in Java projects. The CK tool is instrumental in assessing various software metrics related to complexity, coupling, and cohesion among others. Our version extends the original functionality by addressing Java dependencies issues that were causing build failures. Additionally, we've introduced new features to track the instantiation frequency of classes and the invocation frequency of methods across the codebase. These enhancements aim to provide deeper insights into object creation patterns and method usage within Java applications, further aiding in the evaluation of code quality and design.
- **[Google Gemini API](https://ai.google.dev/):** An AI tool that can be used to analyze the data and metadata generated by the PyDriller and RefactoringMiner. The Gemini API can provide insights into the quality of the code and the refactorings detected, helping to identify good examples for educational purposes. By integrating the Gemini API into our research, we aim to enhance the selection of code examples that demonstrate effective practices for code improvement in Distributed Systems (DS
- **[PyDriller](https://github.com/ishepard/pydriller):** A Python library for mining software repositories, facilitating the extraction of changes, contributions, and evolution of code.
- **[RefactoringMiner](https://github.com/tsantalis/RefactoringMiner):** Specialized in identifying and analyzing source code refactorings in Java repositories, providing insights into code evolution and quality improvement.

## Conclusion

This research methodology, underpinned by detailed code metric analysis and tool integration, aims to offer significant insights into the evolution of software quality in DS. By identifying and analyzing patterns of improvement, this work contributes to the broader field of Software Engineering, particularly in educational contexts where real-world examples of code evolution are invaluable.

## How to Cite?

If you use the Worked Example Miner (WEM) in your research, please cite it using the following BibTeX entry:

```
@misc{softwareWEM:2023,
  title = {Worked Example Miner (WEM): A Comprehensive Tool for Analyzing Java Repositories},
  author = {Breno Farias da Silva},
  year = {2023},
  howpublished = {https://github.com/BrenoFariasdaSilva/Worked-Example-Miner},
  note = {Accessed on September 11, 2024}
}
```

Additionally, a `main.bib` file is available in the root directory of this repository. It contains the BibTeX entry for this project, as well as papers and references related to the research and data made with the Worked Example Miner (WEM).

If you find this repository valuable, please don't forget to give it a ⭐ to show your support! Contributions are highly encouraged, whether by creating issues for feedback or submitting pull requests (PRs) to improve the project. For details on how to contribute, please refer to the [Contributing](#contributing) section below.

Thank you for your support and for recognizing the contribution of this tool to your work!

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. If you have suggestions for improving the code, your insights will be highly welcome.
In order to contribute to this project, please follow the guidelines below or read the [CONTRIBUTING.md](CONTRIBUTING.md) file for more details on how to contribute to this project, as it contains information about the commit standards and the entire pull request process.
Please follow these guidelines to make your contributions smooth and effective:

1. **Set Up Your Environment**: Ensure you've followed the setup instructions in the [Setup](#setup) section to prepare your development environment.

2. **Make Your Changes**:
   - **Create a Branch**: `git checkout -b feature/YourFeatureName`
   - **Implement Your Changes**: Make sure to test your changes thoroughly.
   - **Commit Your Changes**: Use clear commit messages, for example:
     - For new features: `git commit -m "FEAT: Add some AmazingFeature"`
     - For bug fixes: `git commit -m "FIX: Resolve Issue #123"`
     - For documentation: `git commit -m "DOCS: Update README with new instructions"`
     - For refactorings: `git commit -m "REFACTOR: Enhance component for better aspect"`
     - For snapshots: `git commit -m "SNAPSHOT: Temporary commit to save the current state for later reference"`
   - See more about crafting commit messages in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

3. **Submit Your Contribution**:
   - **Push Your Changes**: `git push origin feature/YourFeatureName`
   - **Open a Pull Request (PR)**: Navigate to the repository on GitHub and open a PR with a detailed description of your changes.

4. **Stay Engaged**: Respond to any feedback from the project maintainers and make necessary adjustments to your PR.

5. **Celebrate**: Once your PR is merged, celebrate your contribution to the project!

## Collaborators

We thank the following people who contributed to this project:

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/BrenoFariasdaSilva" title="Breno Farias da Silva">
        <img src="https://github.com/BrenoFariasdaSilva/Worked-Example-Miner/blob/main/.assets/Images/BrenoFarias.jpg" width="100px;" alt="My Profile Picture"/><br>
        <sub>
          <b><a href="https://github.com/BrenoFariasdaSilva">Breno Farias da Silva</a></b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#" title="Marco Aurélio Graciotto Silva">
        <img src="https://github.com/BrenoFariasdaSilva/Worked-Example-Miner/blob/main/.assets/Images/Github.svg" width="100px;" alt="Profile Picture"/><br>
        <sub>
          <b><a href="https://github.com/MAGSilva">Marco Aurélio Graciotto Silva</a></b>
        </sub>
      </a>
    </td>
  </tr>
</table>

## License

This project is licensed under the [Apache License 2.0](LICENSE). This license permits use, modification, distribution, and sublicense of the code for both private and commercial purposes, provided that the original copyright notice and a disclaimer of warranty are included in all copies or substantial portions of the software. It also requires a clear attribution back to the original author(s) of the repository. For more details, see the [LICENSE](LICENSE) file in this repository.
