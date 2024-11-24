<div align="center">

![Logo of Ovadare](./docs/ovadare_logo.png)

# **Ovadare**

🤖 **Ovadare**: Cutting-edge framework for detecting, classifying, and resolving conflicts autonomously. Designed to integrate seamlessly with Autogen and other AI platforms, Ovadare empowers multi-agent systems to handle complex tasks collaboratively and efficiently.

<h3>

[Homepage](https://www.ovadare.com/) | [Documentation](https://docs.ovadare.com/) | [Examples](https://github.com/ovadare/ovadare-examples)

</h3>

[![GitHub Repo stars](https://img.shields.io/github/stars/ovadare/ovadare)](https://github.com/ovadare/ovadare)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

</div>

## Table of contents

- [Why Ovadare?](#why-ovadare)
- [Getting Started](#getting-started)
- [Key Features](#key-features)
- [Examples](#examples)
  - [Conflict Detection](#conflict-detection)
  - [Policy Adjustment](#policy-adjustment)
  - [Resolution Automation](#resolution-automation)
- [Integration with Autogen](#integration-with-autogen)
- [Contribution](#contribution)
- [License](#license)

## Why Ovadare?

In a world where multi-agent systems are becoming the backbone of AI-driven solutions, Ovadare stands out by providing robust conflict detection, classification, and resolution capabilities. Whether it's resolving task overlaps, prioritization issues, or behavioral conflicts among agents, Ovadare ensures seamless collaboration within your AI ecosystem.

## Getting Started

To get started with Ovadare, follow these simple steps:

### 1. Installation

Ensure you have Python >=3.8 installed on your system. Ovadare can be installed via pip:

''
pip install ovadare
''

### 2. Setting Up Ovadare

To integrate Ovadare into your project, create an Ovadare conflict resolution manager:

''
from ovadare.conflicts import ConflictDetector, ConflictResolver

detector = ConflictDetector()
resolver = ConflictResolver()

# Detect conflicts
conflicts = detector.detect_conflicts(agent_data)

# Resolve conflicts
resolved = resolver.resolve_conflicts(conflicts)
''

### 3. Configuring Policies

Ovadare allows you to define custom policies for conflict resolution:

''
from ovadare.policies import PolicyManager, Policy

policy_manager = PolicyManager()

custom_policy = Policy(
    name="TaskPrioritization",
    rules=[
        "If two agents are assigned the same task, prioritize based on expertise.",
        "Resolve resource allocation conflicts using weighted scoring."
    ]
)

policy_manager.add_policy(custom_policy)
''

### 4. Running with Autogen

Ovadare integrates seamlessly with Autogen for multi-agent orchestration. Define agents and tasks using Autogen and let Ovadare handle the conflicts:

''
from autogen import Agent, Task

agents = [
    Agent(name="Agent1", role="Planner"),
    Agent(name="Agent2", role="Executor")
]

tasks = [
    Task(name="Plan Project", assigned_to="Agent1"),
    Task(name="Execute Project", assigned_to="Agent2"),
]

# Detect and resolve conflicts before execution
conflicts = detector.detect_conflicts(tasks)
resolved_tasks = resolver.resolve_conflicts(conflicts)
''

## Key Features

- **Comprehensive Conflict Handling**: Detect, classify, and resolve agent-level conflicts.
- **Customizable Policies**: Define dynamic policies tailored to your specific needs.
- **Seamless Integration**: Works out-of-the-box with platforms like Autogen.
- **Extensibility**: Easily extend functionality with custom rules and modules.
- **Advanced Analytics**: Monitor and visualize conflict trends and resolution effectiveness.

## Examples

### Conflict Detection

Detect conflicts in a multi-agent system with ease:

''
conflicts = detector.detect_conflicts(agent_tasks)
print(conflicts)
''

### Policy Adjustment

Dynamically adjust policies based on feedback loops:

''
policy_manager.adjust_policy("TaskPrioritization", new_rules=["If deadlines conflict, prioritize by urgency."])
''

### Resolution Automation

Automate resolution using AI-powered decision-making engines:

''
resolved = resolver.resolve_conflicts(conflicts, method="ai-assisted")
''

## Integration with Autogen

Ovadare enhances Autogen by adding robust conflict resolution capabilities to its agent orchestration framework. By integrating Ovadare, you can ensure that your agents collaborate effectively without stepping on each other's toes.

## Contribution

Ovadare is open-source, and we welcome contributions. To contribute:

1. Fork the repository.
2. Create a new branch for your feature.
3. Add your feature or improvement.
4. Send a pull request.

### Running Tests

''
pytest tests/
''

### Static Analysis

''
mypy ovadare/
''

### Packaging

''
python setup.py sdist bdist_wheel
''

## License

Ovadare is released under the [MIT License](https://github.com/ovadare/ovadare/blob/main/LICENSE).
