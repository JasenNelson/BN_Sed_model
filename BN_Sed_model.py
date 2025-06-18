# =============================================================================
# Proof-of-Concept Bayesian Network for BC Sediment Quality Assessment
# =============================================================================
#
# Author: Expert Team, AI-Driven Scientific Framework Project
# Date:
#
# Description:
# This script creates a proof-of-concept Bayesian Network (BN) to model the
# relationships between sediment contaminants, environmental modifiers, and
# ecological effects in British Columbia aquatic ecosystems. It uses the
# 'pgmpy' library to define the model structure and parameterize it with
# illustrative Conditional Probability Tables (CPTs) derived from a
# synthesis of scientific literature.
#
# Purpose:
# This code serves as a tangible demonstration of the methodology proposed
# in the main framework document. It is not intended for direct regulatory
# use but as a blueprint for a future, fully data-parameterized model.
#
# Libraries Required:
# - pgmpy
# - pandas
# - networkx (usually installed with pgmpy)
#
# To install necessary libraries:
# pip install pgmpy pandas networkx

# --- 1. Import Libraries ---
from pgmpy.models import DiscreteBayesianNetwork  # Fixed: Changed from BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# --- 2. Define the Bayesian Network Structure ---
# The structure is defined as a list of tuples, where each tuple represents
# a directed edge (from_node, to_node) in the Directed Acyclic Graph (DAG).
# This structure is based on the conceptual model developed in Phase 1.
# [23, 24, 27]

# <<< COMPLETED: Defined the model structure based on the parent-child
# relationships in the CPTs defined below.
model_structure = [
    ('Contaminant_Conc', 'Bioavailability'),
    ('TOC', 'Bioavailability'),
    ('Grain_Size', 'Bioavailability'),
    ('Bioavailability', 'Ecological_Effect'),
    ('Benthic_Community_Type', 'Ecological_Effect'),
    ('Ecological_Effect', 'Mortality_Growth'),
    ('Ecological_Effect', 'Community_Richness')
]


# Initialize the DiscreteBayesianNetwork object
# [60, 63]
model = DiscreteBayesianNetwork(model_structure)  # Fixed: Changed from BayesianNetwork

print("Model Structure Defined:")
print(f"Nodes: {model.nodes()}")
print(f"Edges: {model.edges()}")
print("-" * 50)


# --- 3. Define Conditional Probability Distributions (CPDs) ---
# Each node in the network requires a CPD. For this proof-of-concept,
# probabilities are illustrative and based on general ecotoxicological
# principles found in the literature.
# A fully operational model would learn these from empirical data.
# [62, 83, 84]

# Node: Contaminant_Conc (Stressor)
# This is a root node (no parents). Its probabilities are prior probabilities.
# States: 0=Low, 1=Medium, 2=High
cpd_contaminant = TabularCPD(
    variable='Contaminant_Conc',
    variable_card=3,
    values=[[0.6], [0.3], [0.1]],  # P(Low)=0.6, P(Med)=0.3, P(High)=0.1
    state_names={'Contaminant_Conc': ['Low', 'Medium', 'High']}
)

# Node: TOC (Total Organic Carbon - Modifier)
# Root node.
# States: 0=Low, 1=High
cpd_toc = TabularCPD(
    variable='TOC',
    variable_card=2,
    values=[[0.5], [0.5]], # Assuming equal probability for demonstration
    state_names={'TOC': ['Low', 'High']}
)

# Node: Grain_Size (Modifier)
# Root node.
# States: 0=Coarse, 1=Fine
cpd_grain_size = TabularCPD(
    variable='Grain_Size',
    variable_card=2,
    values=[[0.5], [0.5]],
    state_names={'Grain_Size': ['Coarse', 'Fine']}
)

# Node: Benthic_Community_Type (Receptor)
# Root node representing the inherent sensitivity of the present community.
# States: 0=Robust, 1=Sensitive (e.g., EPT-dominated) [46, 55]
cpd_benthic_community = TabularCPD(
    variable='Benthic_Community_Type',
    variable_card=2,
    values=[[0.6], [0.4]],
    # <<< COMPLETED: Added state names for this node.
    state_names={'Benthic_Community_Type': ['Robust', 'Sensitive']}
)

# Node: Bioavailability (Mediating Process)
# Parents: Contaminant_Conc, TOC, Grain_Size
# Logic: Bioavailability is highest with high contamination, low TOC, and coarse grains.
# It is lowest with low contamination, high TOC, and fine grains. [15, 18]
# States: 0=Low, 1=High
# The values table is structured with columns representing all combinations of parent states.
# Order of evidence: Contaminant_Conc, TOC, Grain_Size
# Columns: (C_L,T_L,G_C), (C_L,T_L,G_F), (C_L,T_H,G_C), (C_L,T_H,G_F),... (C_H,T_H,G_F)
cpd_bioavailability = TabularCPD(
    variable='Bioavailability',
    variable_card=2,
    values=[
        # C=Low   C=Med   C=High
        [0.99, 0.95, 0.90, 0.80, 0.80, 0.60, 0.50, 0.30, 0.40, 0.20, 0.10, 0.05], # P(Bioavailability=Low)
        [0.01, 0.05, 0.10, 0.20, 0.20, 0.40, 0.50, 0.70, 0.60, 0.80, 0.90, 0.95]  # P(Bioavailability=High)
    ],
    # <<< COMPLETED: Added the evidence (parent nodes) and their cardinalities (number of states).
    evidence=['Contaminant_Conc', 'TOC', 'Grain_Size'],
    evidence_card=[3, 2, 2],
    state_names={
        'Bioavailability': ['Low', 'High'],
        'Contaminant_Conc': ['Low', 'Medium', 'High'],
        'TOC': ['Low', 'High'],
        'Grain_Size': ['Coarse', 'Fine']
    }
)

# Node: Ecological_Effect (Mediating Process)
# Parents: Bioavailability, Benthic_Community_Type
# Logic: Severe effects are most probable with high bioavailability and a sensitive community.
# States: 0=None, 1=Moderate, 2=Severe
cpd_eco_effect = TabularCPD(
    variable='Ecological_Effect',
    variable_card=3,
    # <<< COMPLETED: Calculated and filled in the first row for P(Effect=None)
    # such that each column sums to 1.
    values=[
        [0.90, 0.70, 0.20, 0.05],  # P(Effect=None)
        [0.09, 0.25, 0.60, 0.35],  # P(Effect=Moderate)
        [0.01, 0.05, 0.20, 0.60]   # P(Effect=Severe)
    ],
    # <<< COMPLETED: Added the evidence (parent nodes) and their cardinalities.
    evidence=['Bioavailability', 'Benthic_Community_Type'],
    evidence_card=[2, 2],
    state_names={
        # <<< COMPLETED: Added state names for this node and its parent.
        'Ecological_Effect': ['None', 'Moderate', 'Severe'],
        'Bioavailability': ['Low', 'High'],
        'Benthic_Community_Type': ['Robust', 'Sensitive']
    }
)

# Node: Mortality_Growth (Endpoint)
# Parent: Ecological_Effect
# Logic: High mortality/growth impairment is a direct result of a severe ecological effect. [53]
# States: 0=Normal, 1=Impaired
cpd_mortality = TabularCPD(
    variable='Mortality_Growth',
    variable_card=2,
    # <<< COMPLETED: Calculated and filled in the first row for P(Mortality=Normal).
    values=[
        [0.98, 0.40, 0.10], # P(Mortality=Normal)
        [0.02, 0.60, 0.90]  # P(Mortality=Impaired)
    ],
    evidence=['Ecological_Effect'],
    # <<< COMPLETED: Added the cardinality for the evidence node.
    evidence_card=[3],
    state_names={
        'Mortality_Growth': ['Normal', 'Impaired'],
        # <<< COMPLETED: Added state names for the parent node.
        'Ecological_Effect': ['None', 'Moderate', 'Severe']
    }
)

# Node: Community_Richness (Endpoint)
# Parent: Ecological_Effect
# Logic: Low community richness is a direct result of a severe ecological effect. [55]
# States: 0=High, 1=Low
cpd_richness = TabularCPD(
    variable='Community_Richness',
    variable_card=2,
    # <<< COMPLETED: Calculated and filled in the first row for P(Richness=High).
    values=[
        [0.95, 0.30, 0.05], # P(Richness=High)
        [0.05, 0.70, 0.95]  # P(Richness=Low)
    ],
    evidence=['Ecological_Effect'],
    # <<< COMPLETED: Added the cardinality for the evidence node.
    evidence_card=[3],
    state_names={
        'Community_Richness': ['High', 'Low'],
        # <<< COMPLETED: Added state names for the parent node.
        'Ecological_Effect': ['None', 'Moderate', 'Severe']
    }
)

# --- 4. Add CPDs to the Model ---
model.add_cpds(
    cpd_contaminant,
    cpd_toc,
    cpd_grain_size,
    cpd_benthic_community,
    cpd_bioavailability,
    cpd_eco_effect,
    cpd_mortality,
    cpd_richness
)

# --- 5. Validate the Model ---
# The check_model() method verifies that the CPDs are defined correctly for
# the model structure and that the probabilities in each CPD sum to 1.
is_valid = model.check_model()
print(f"Is the model valid? {is_valid}")
if not is_valid:
    raise ValueError("Model is not valid. Check structure and CPDs.")
print("-" * 50)

# --- 5.1 Save the Model ---
print("Saving model to 'bn_sed_model.pkl'...")
import pickle

with open('bn_sed_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("Model saved successfully!")
print("-" * 50)

# --- 6. Perform Probabilistic Inference ---
# Initialize the inference engine. VariableElimination is a common exact
# inference algorithm. [36]
inference = VariableElimination(model)

# --- Example 1: Forward Inference (Prediction) ---
# Question: What is the probability of a severe ecological effect if we know
# the contaminant concentration is High, TOC is Low, and the community is Sensitive?
print("Example 1: Forward Inference (Prediction)")
query_result_1 = inference.query(
    variables=['Ecological_Effect'],
    evidence={
        'Contaminant_Conc': 'High',
        'TOC': 'Low',
        'Benthic_Community_Type': 'Sensitive'
    }
)
print(query_result_1)
print("-" * 50)


# --- Example 2: Inverse Inference (Diagnosis) ---
# This demonstrates the power of BNs for standard setting.
# Question: To ensure the probability of a 'Severe' ecological effect is very low
# (e.g., we observe 'None' or 'Moderate' effect), what is the most likely
# state of the contaminant concentration?
# This simulates setting a protection goal and finding the conditions consistent with it.
# [36, 37, 81]
print("Example 2: Inverse Inference (Standard Setting Simulation)")
query_result_2 = inference.query(
    variables=['Contaminant_Conc'],
    evidence={
        'Ecological_Effect': 'None' # Evidence: We observe no ecological effect
    }
)
print("Posterior probability of Contaminant Concentration given NO ecological effect:")
print(query_result_2)
print("\nNote how the probability of 'Low' concentration has increased significantly from the prior.")
print("-" * 50)

# --- Example 3: What-if Scenario ---
# Question: Compare the risk to a sensitive vs. a robust community, holding
# other factors constant at a high-risk setting.
print("Example 3: Comparing Scenarios")
# Scenario A: Robust Community
risk_robust = inference.query(
    variables=['Ecological_Effect'],
    evidence={'Contaminant_Conc': 'High', 'TOC': 'Low', 'Benthic_Community_Type': 'Robust'}
)
print("Predicted Effect for a ROBUST community in a high-risk setting:")
print(risk_robust)

# Scenario B: Sensitive Community
risk_sensitive = inference.query(
    variables=['Ecological_Effect'],
    evidence={'Contaminant_Conc': 'High', 'TOC': 'Low', 'Benthic_Community_Type': 'Sensitive'}
)
print("\nPredicted Effect for a SENSITIVE community in the same high-risk setting:")
print(risk_sensitive)
print("\nThis demonstrates the model's ability to quantify the impact of receptor sensitivity.")
print("-" * 50)