import numpy as np
from dataclasses import dataclass
from typing import List, Dict

# --- CORE DATA STRUCTURES ---

@dataclass
class Entity:
    """
    Represents a real-world object (Person, Location, Asset)
    as a State Vector in the Universal Matrix.
    """
    id: str
    type: str  # e.g., 'student', 'traffic_node', 'market'
    # The 'DNA' of the entity: [Value, Risk, Potential, Health]
    state_vector: np.ndarray 

class UniversalMatrixEngine:
    """
    The central processor that ingests entities and optimizes
    their relationships using Linear Algebra.
    """
    def __init__(self):
        self.registry: Dict[str, Entity] = {}
        self.interaction_matrix = None # The Global Adjacency Matrix

    def register_entity(self, entity_id: str, type_label: str, initial_data: List[float]):
        """
        Ingests a new node into the system.
        Example: Adding a Student with [Grades, Attendance, GitHub_Commits]
        """
        vector = np.array(initial_data, dtype=float)
        # Normalize vector (0-1 scale) for universal compatibility
        normalized_vector = vector / (np.linalg.norm(vector) + 1e-9)
        
        new_entity = Entity(id=entity_id, type=type_label, state_vector=normalized_vector)
        self.registry[entity_id] = new_entity
        print(f"[MATRIX] Entity Registered: {entity_id} | Vector Magnitude: {np.linalg.norm(normalized_vector):.4f}")

    def calculate_compatibility(self, entity_a_id: str, entity_b_id: str) -> float:
        """
        Calculates the 'Trust' or 'Value' link between two separate entities
        using Dot Product Similarity.
        """
        vec_a = self.registry[entity_a_id].state_vector
        vec_b = self.registry[entity_b_id].state_vector
        
        # Mathematical alignment calculation
        compatibility_score = np.dot(vec_a, vec_b)
        return compatibility_score

    def optimize_decision(self, target_id: str, candidates: List[str]):
        """
        The 'Oracle' Function. Finds the best match for a target.
        Example: Matching a Student (target) to the best Job (candidate).
        """
        best_match = None
        highest_score = -1.0
        
        print(f"\n--- OPTIMIZING FOR: {target_id} ---")
        for candidate_id in candidates:
            score = self.calculate_compatibility(target_id, candidate_id)
            print(f" > Analyzing Link: {candidate_id} ... Score: {score:.4f}")
            
            if score > highest_score:
                highest_score = score
                best_match = candidate_id
                
        print(f"--- OPTIMAL SOLUTION: {best_match} (Efficiency: {highest_score*100:.1f}%) ---\n")
        return best_match

# --- SIMULATION: THE 'SKILLS ORACLE' SCENARIO ---

if __name__ == "__main__":
    # Initialize the Engine
    Matrix = UniversalMatrixEngine()

    # 1. Define a User (e.g., A LASUSTECH Student)
    # Vector Attributes: [Coding_Skill, Math_Skill, Communication, Availability]
    Matrix.register_entity("User_Airneyx", "student", [0.9, 0.8, 0.6, 1.0])

    # 2. Define Market Opportunities (Jobs)
    # Requirements Vector: [Coding_Need, Math_Need, Comm_Need, Urgency]
    Matrix.register_entity("Job_Google", "corp", [0.95, 0.9, 0.8, 0.5])
    Matrix.register_entity("Job_Local_Startup", "sme", [0.8, 0.6, 0.9, 0.9])
    Matrix.register_entity("Job_Freelance_Gig", "gig", [0.85, 0.5, 0.4, 1.0])

    # 3. Run The Optimization
    # The System decides the best path for the User
    Matrix.optimize_decision("User_Airneyx", ["Job_Google", "Job_Local_Startup", "Job_Freelance_Gig"])
