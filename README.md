<div align="center">
   
# [Scientific Research](https://github.com/BrenoFariasdaSilva/Scientific-Research) <img src="https://github.com/BrenoFariasdaSilva/Scientific-Research/blob/main/.assets/Bash.svg"  width="3%" height="3%">

</div>

<div align="center">
  
---

Welcome to my Scientific Research Repository! This repository contains code and data related to my ongoing scientific research project. Our team is focused on various goals, as described below.
  
---

</div>

<div align="center">

![GitHub Code Size in Bytes](https://img.shields.io/github/languages/code-size/BrenoFariasdaSilva/Scientific-Research)
![GitHub Last Commit](https://img.shields.io/github/last-commit/BrenoFariasdaSilva/Scientific-Research)
![GitHub](https://img.shields.io/github/license/BrenoFariasdaSilva/Scientific-Research)
![wakatime](https://wakatime.com/badge/github/BrenoFariasdaSilva/Scientific-Research.svg)

</div>

<div align="center">
   
![Repobeats Statistics](https://repobeats.axiom.co/api/embed/cc926b338fcd1c49112ae0c1707e41cbfc07f606.svg "Repobeats analytics image")

</div>

## Table of Contents
- [Scientific Research ](#scientific-research-)
  - [Table of Contents](#table-of-contents)
  - [Goals](#goals)
  - [Skills](#skills)
  - [Directories](#directories)
  - [Tools](#tools)
  - [Repositories](#repositories)
    - [Apache Commons-lang](#apache-commons-lang)
    - [JabRef](#jabref)
  - [License](#license)

## Goals

1. **Similarity Analysis:**
   - We analyze different similarity algorithms, including Word2Vector, Yake, Sentence Bert, and TF-IDF (Term Frequency - Inverse Document Frequency) to evaluate the similarity between texts.
   - We create two datasets based on these similarity calculations: one for storing solved (answered) questions and another for storing unsolved questions.
   - Using these datasets, we determine the most similar solved questions for each unsolved question and auto-recommend changes based on the similarity of those questions.

2. **Enhancing Code Solutions:**
   - We study the use of tools like ChatGPT and GitHub Copilot to improve students' code solutions when they are stuck.
   - Currently, we utilize CK to generate Code Metrics for repositories like Apache Commons-lang and Jabref.
   - We employ PyDriller to traverse the commit tree in the repository and run CK for every commit hash it is in.
   - This allows us to gather code metrics such as CBO, CBOModified, WMC, RFC, and others to create graphics depicting the metrics evolution of specific classes or methods within the repository.

3. **Analyzing Code Evolution:**
   - With the collected data and code metrics, we analyze code that started with "bad" metrics and evolved over time.
   - We aim to identify good code examples that indicate what makes code better and what changes are typically made to improve it.

4. **Providing Data to AI Tools:**
   - We gather valuable data to provide to tools like ChatGPT and GitHub Copilot, showcasing what constitutes good code and why.
   - We explore how contextual information, such as code samples, can assist these tools in suggesting better code improvements for students.

## Skills

Our research project involves expertise in the following areas:

- CK
- PyDriller
- RefactoringMiner
- Word2Vector
- Pandas
- NumPy
- Matplotlib
- Scikit-Learn
- Statistical Data Analysis
- Similarity measures
- Apache Commons-lang
- Jabref
- Code metrics
- Python (Programming Language)

Feel free to explore the code and data in this repository. If you have any questions or suggestions, please don't hesitate to reach out to me.

## Directories

Each directory in this repository has its own README.md file explaining its purpose. Please refer to individual README files for more details.

## Tools

- **CK (Code Klatt):** A tool used to collect and analyze code metrics from repositories. In this project, CK is employed to generate code metrics for repositories like Apache Commons-lang and Jabref.

- **PyDriller:** A Python framework used for mining software repositories. It is utilized to traverse the commit tree in the repository and run CK for every commit hash it is in.

- **RefactoringMiner:** A tool used for mining refactorings in Git repositories. It helps identify changes in the code that contribute to code evolution.

- **Word2Vector:** A technique used for natural language processing and understanding. In this project, Word2Vector is employed for similarity analysis between texts, such as code snippets and questions.

## Repositories

### [Apache Commons-lang](https://github.com/apache/commons-lang)

- **Purpose:** Apache Commons Lang is a library with helper utilities for the java.lang API, notably String manipulation methods, basic numerical methods, object reflection, and more.
- **Usage in Research:** We leverage this repository to study code evolution and gather code metrics using CK.

### [JabRef](https://github.com/JabRef/jabref)

- **Purpose:** JabRef is an open-source bibliography reference manager that uses BibTeX as its native format.
- **Usage in Research:** We utilize JabRef to analyze code solutions, extract code metrics using CK, and understand the code evolution of a real-world application.

Feel free to explore these repositories to gain insights into our research and methodologies.

## License

This project is licensed under the [Creative Commons Zero v1.0 Universal](LICENSE), which means you are free to use, modify, and distribute the code, as long as you mention include the license and attribute you as the original author for the repository. See the [LICENSE](LICENSE) file for more details.
