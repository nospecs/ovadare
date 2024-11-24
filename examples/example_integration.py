# example_integration.py

from ovadare.conflicts.conflict_detector import ConflictDetector
from ovadare.conflicts.conflict_resolver import ConflictResolver
from ovadare.policies.policy_manager import PolicyManager, Policy
from ovadare.agents.agent import Agent

def main():
    # Initialize Policy Manager
    policy_manager = PolicyManager()

    # Define Policies
    read_policy = Policy(
        name='ReadPolicy',
        rules={
            'access_level': 'read',
            'resource_limits': 'moderate'
        }
    )
    write_policy = Policy(
        name='WritePolicy',
        rules={
            'access_level': 'write',
            'resource_limits': 'high'
        }
    )

    # Add Policies to Policy Manager
    policy_manager.add_policy(read_policy)
    policy_manager.add_policy(write_policy)

    # Initialize Agents with Policies
    agent_a = Agent(
        name='AgentA',
        role='DataProcessor',
        policies=[read_policy]
    )
    agent_b = Agent(
        name='AgentB',
        role='DataAnalyzer',
        policies=[write_policy]
    )

    # Simulate Agent Actions
    # AgentA attempts to write data, which should cause a policy conflict
    agent_a_action = {
        'agent': agent_a.name,
        'action': 'write_data',
        'resource': 'Dataset1'
    }
    agent_b_action = {
        'agent': agent_b.name,
        'action': 'read_data',
        'resource': 'Dataset1'
    }

    # Collect Actions
    agent_actions = [agent_a_action, agent_b_action]

    # Initialize Conflict Detector
    conflict_detector = ConflictDetector()

    # Detect Conflicts
    conflicts = conflict_detector.detect_conflicts(
        agent_actions=agent_actions,
        policy_manager=policy_manager
    )

    # Check if any conflicts were detected
    if conflicts:
        print("Conflicts detected:")
        for conflict in conflicts:
            print(conflict)

        # Initialize Conflict Resolver
        conflict_resolver = ConflictResolver()

        # Resolve Conflicts
        resolutions = conflict_resolver.resolve_conflicts(conflicts)

        print("\nResolutions:")
        for resolution in resolutions:
            print(resolution)
    else:
        print("No conflicts detected. Agents can proceed with their actions.")

    # Integration with Autogen for Automated Testing
    # Set up Autogen Assistant Agent for generating test cases
    test_agent = AssistantAgent(
        name='TestAgent',
        system_prompt='You are an expert in testing Ovadare\'s conflict detection capabilities.',
        model='gpt-4'
    )

    # Define a test scenario
    test_scenario = """
    Given AgentA with read-only access tries to write data to Dataset1,
    and AgentB with write access reads data from Dataset1,
    test that a policy conflict is detected for AgentA and resolved appropriately.
    """

    # Run the test scenario
    test_response = test_agent.run(test_scenario)
    print("\nAutogen Test Agent Response:")
    print(test_response)

if __name__ == '__main__':
    main()
