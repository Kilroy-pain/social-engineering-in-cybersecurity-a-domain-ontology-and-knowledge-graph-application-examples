import networkx as nx
import numpy as np

class SocialEngineeringOntology:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.define_ontology()

    def define_ontology(self):
        # Define core entities (nodes)
        entities = [
            "Attacker", "Victim", "HumanVulnerability", "AttackMedium",
            "AttackTechnique", "AttackPath", "SocialEngineeringScenario",
            "Incident", "ThreatElement", "Target", "Origin"
        ]
        self.graph.add_nodes_from(entities)

        # Define relations (edges)
        relations = [
            ("Attacker", "AttackTechnique"),
            ("AttackTechnique", "AttackMedium"),
            ("AttackMedium", "HumanVulnerability"),
            ("HumanVulnerability", "Victim"),
            ("Victim", "Incident"),
            ("Incident", "SocialEngineeringScenario"),
            ("SocialEngineeringScenario", "ThreatElement"),
            ("ThreatElement", "Target"),
            ("Attacker", "Target"),
            ("Attacker", "Origin"),
            ("Origin", "AttackPath"),
            ("AttackPath", "Target"),
        ]
        self.graph.add_edges_from(relations)

    def add_attack_scenario(self, scenario_name, attacker, victim, technique, medium, vulnerability, incident):
        # Add nodes and edges for a specific attack scenario
        self.graph.add_node(scenario_name, type="Scenario")
        self.graph.add_edge(attacker, technique)
        self.graph.add_edge(technique, medium)
        self.graph.add_edge(medium, vulnerability)
        self.graph.add_edge(vulnerability, victim)
        self.graph.add_edge(victim, incident)
        self.graph.add_edge(incident, scenario_name)

    def find_top_ranked_elements(self, node_type):
        # Find top-ranked elements based on degree centrality
        centrality = nx.degree_centrality(self.graph)
        ranked_elements = sorted(
            [(node, centrality[node]) for node in self.graph.nodes if self.graph.nodes[node].get("type") == node_type],
            key=lambda x: x[1],
            reverse=True
        )
        return ranked_elements

    def find_potential_threats(self, victim):
        # Find potential threats to a victim
        threats = list(nx.descendants(self.graph, victim))
        return threats

    def find_potential_targets(self, attacker):
        # Find potential targets for an attacker
        targets = list(nx.descendants(self.graph, attacker))
        return targets

    def find_attack_paths(self, attacker, target):
        # Find all paths from attacker to target
        paths = list(nx.all_simple_paths(self.graph, source=attacker, target=target))
        return paths

    def analyze_same_origin_attacks(self, origin):
        # Analyze attacks originating from the same origin
        origin_attacks = list(nx.descendants(self.graph, origin))
        return origin_attacks

if __name__ == '__main__':
    # Initialize ontology
    ontology = SocialEngineeringOntology()

    # Add dummy attack scenarios
    ontology.add_attack_scenario(
        scenario_name="PhishingAttack1",
        attacker="Attacker1",
        victim="Victim1",
        technique="Phishing",
        medium="Email",
        vulnerability="Trust",
        incident="DataBreach1"
    )

    ontology.add_attack_scenario(
        scenario_name="PhishingAttack2",
        attacker="Attacker2",
        victim="Victim2",
        technique="Phishing",
        medium="SocialMedia",
        vulnerability="Curiosity",
        incident="DataBreach2"
    )

    # Demonstrate functionalities
    print("Top-ranked elements (by degree centrality):")
    print(ontology.find_top_ranked_elements("Scenario"))

    print("\nPotential threats to Victim1:")
    print(ontology.find_potential_threats("Victim1"))

    print("\nPotential targets for Attacker1:")
    print(ontology.find_potential_targets("Attacker1"))

    print("\nAttack paths from Attacker1 to Victim1:")
    print(ontology.find_attack_paths("Attacker1", "Victim1"))

    print("\nAnalyze same origin attacks from Origin:")
    print(ontology.analyze_same_origin_attacks("Origin"))