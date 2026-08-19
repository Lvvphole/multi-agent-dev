# Problem-to-Retained-Revenue Operating System

Status: Approved organizational operating specification.
Owner and consequential decision authority: Lvvphole.

## 1. Purpose

The business exists to repeatedly identify a valuable client state change, cause that state change, capture part of the created value, maintain the exchange while it remains mutually valuable, and use the resulting evidence to improve the next decision.

The organizational goal is:

> Repeatedly create, deliver, verify, and retain economically sustainable client value.

The system must produce both:

- `REALIZED_CLIENT_VALUE`: the client's important current state moved toward or reached the agreed desired state.
- `SUSTAINABLE_RETAINED_REVENUE`: the business captured sufficient economic value to continue producing the client outcome.

Revenue is an intermediate result. It proves that both parties accepted an expected exchange. It does not prove that the promised client state change occurred.

## 2. Desired state

The desired business state is a repeatable closed-loop system that continuously:

1. finds consequential client problems;
2. validates that each problem is real, unsatisfied, consequential, reachable, and solvable;
3. diagnoses the causal gap;
4. designs an intervention that is materially better than available alternatives;
5. reaches qualified clients and moves them through observable behavioral states;
6. captures an economically viable commitment;
7. implements the intervention;
8. verifies the client outcome;
9. retains or intentionally ends the economic relationship; and
10. returns evidence and learning to the next cycle.

For every active value cycle, the system must be able to answer:

1. Which client has an important gap?
2. Why does the gap exist?
3. What intervention can close it?
4. Did the intervention close it?
5. Is enough value being created for both parties to continue the relationship?

## 3. Objective functions

### 3.1 Client value

Client value is:

```text
V_C = Expected Desired-State Improvement - Total Customer Sacrifice
```

Expected desired-state improvement contains:

```text
Outcome Magnitude * Probability * Durability
```

Total customer sacrifice contains:

```text
Money + Time + Effort + Risk + Disruption + Opportunity Cost
```

The client objective is the greatest predictable desired-state improvement with the least necessary customer sacrifice. Necessary qualification, implementation, commitment, and learning effort must not be confused with avoidable friction.

### 3.2 Business value

The business objective is:

```text
maximize over operating policy pi:
E[sum from t=0 to infinity of gamma^t * RG_t]
```

Where:

- `pi` is the operating policy;
- `RG_t` is retained gross profit or contribution at time `t`; and
- `gamma` represents the value of future economic returns.

This objective is admissible only while:

- `V_C > 0`;
- `LTV > CAC` at the applicable decision level;
- the client outcome is verified; and
- risk remains within permitted limits.

The business maximizes economically viable retained value exchange, not transactions.

## 4. Fundamental state model

Every opportunity uses this state model:

```text
S_C -> G -> I -> S_D -> V_R
```

- `S_C`: verified current state.
- `G`: gap between the current and desired states.
- `I`: intervention intended to close the gap.
- `S_D`: observable desired state.
- `V_R`: realized value established from observed effect.

Conceptually:

```text
G = S_D - S_C
```

Each implementation must define a valid domain-specific comparison. The notation does not authorize subtraction of incompatible, ordinal, or unmeasured states.

The fundamental business question is: can the organization close an important client gap more effectively than the client's current alternative?

## 5. Canonical operating loop

The system has **12 operating stages**, numbered `0` through `11`:

| Stage | Name | System question | Required output |
| --- | --- | --- | --- |
| 0 | Objective Definition | What result are we trying to create? | Goal, current state, desired state, definition of done, objective function, constraints |
| 1 | Problem Scouting | Where do consequential gaps exist? | Candidate problems |
| 2 | Problem Validation | Is the problem real and commercially useful? | Verified problem |
| 3 | Gap Diagnosis | Why does the problem exist? | Causal gap model |
| 4 | Solution Design | What intervention can close the gap? | Testable value hypothesis and solution |
| 5 | Distribution | How do we reach the correct market? | Qualified reach |
| 6 | Demand Generation | How do we create or capture willingness to act? | Qualified commercial interest |
| 7 | Behavioral Progression | What prevents the buyer from moving? | Verified buyer state transitions |
| 8 | Revenue | Will both parties commit to the exchange? | Commercial agreement |
| 9 | Implementation | Does the intervention change the target behavior? | Verified target behavior change |
| 10 | Value Realization | Did the desired client state occur? | Verified client value |
| 11 | Retention and Expansion | Is continued exchange valuable? | Retained or expanded revenue, or intentional exit |

The canonical sequence is:

```text
Stage 0 Objective Definition
  -> Stage 1 Problem Scouting
  -> Stage 2 Problem Validation
  -> Stage 3 Gap Diagnosis
  -> Stage 4 Solution Design
  -> Stage 5 Distribution
  -> Stage 6 Demand Generation
  -> Stage 7 Behavioral Progression
  -> Stage 8 Revenue
  -> Stage 9 Implementation
  -> Stage 10 Value Realization
  -> Stage 11 Retention and Expansion
  -> Stage 0 Objective Definition revalidation
  -> Stage 1 Problem Scouting
```

The normalized return invariant is `Stage 11 -> Stage 0 -> Stage 1`. Stage 0 revalidates the goal, desired state, objective function, constraints, and definition of done. If they remain valid, the cycle continues without changing them.

## 6. Definition of done and terminal states

The business has no permanent terminal state. Completion applies to one client value cycle.

A value cycle can close only when the record contains evidence for:

- a verified problem;
- a defined desired state;
- a diagnosed gap;
- a delivered solution;
- a verified target behavior change;
- a verified desired outcome;
- captured revenue;
- retained or intentionally terminated economic exchange; and
- learning returned to the operating system.

Terminal states have distinct meanings:

- `CLOSED_SUCCESS`: verified client value, viable retained or expanded revenue, and captured learning.
- `CLOSED_EXIT`: the relationship was intentionally ended and learning was captured. This closes the cycle but is not retained-revenue success.
- `BLOCKED`: required evidence, authority, capability, or viable progression is unavailable. `BLOCKED` is not success.
- `FAIL`: the intervention or operating process failed its acceptance conditions.
- `CANCELLED`: Lvvphole ended the cycle before its outcome was established.

A signed contract, completed implementation, product usage, or agent completion claim cannot independently close a value cycle.

## 7. Stage contracts

### 7.1 Stage 0: Objective Definition

Required fields are goal, current state, desired state, definition of done, objective function, and constraints. No optimization or stage progression may begin while a required field is unresolved.

### 7.2 Stage 1: Problem Scouting

Search for repeated workarounds, delays, waste, lost revenue, excessive cost, risk, dissatisfaction, manual effort, unmet expectations, failed alternatives, environmental changes, behavioral changes, and new limitations created by existing solutions.

The output is a candidate problem, not a validated opportunity or solution.

### 7.3 Stage 2: Problem Validation

The candidate must pass all five gates:

```text
Real * Unsatisfied * Consequential * Reachable * Solvable
```

Failure at any gate prevents solution design and returns evidence to scouting. The ICP is represented as entity, context, problem, consequence, and ability to act.

### 7.4 Stage 3: Gap Diagnosis

Diagnose:

```text
Current Solution
  -> Limitation
  -> Verified Need
  -> Target Behavior
  -> Constraint
```

A limitation is observed evidence. A verified need is the required improvement. A target behavior states what must change. A constraint explains why the target behavior is not occurring.

### 7.5 Stage 4: Solution Design

Do not design the intervention before diagnosing the constraint. Use this causal chain:

```text
Constraint
  -> Mechanism
  -> Intervention
  -> Behavior Change
  -> Desired Outcome
```

Every solution requires a testable value hypothesis:

```text
For ICP X, intervention I should change behavior B because mechanism M
removes constraint C, producing outcome O.
```

The intervention can be a product, service, offer, process, technology, or experience. It is not value until the state change is observed.

### 7.6 Stage 5: Distribution

Optimize qualified reach, not raw reach. The stage must identify the correct client, channel, receptive condition, acquisition cost, and potential compounding distribution asset.

### 7.7 Stage 6: Demand Generation

Support three motions:

- demand creation: make a qualified client recognize and prioritize a problem;
- demand capture: identify qualified clients already showing relevant intent; and
- demand expansion: identify a consequential new gap inside an existing client.

For complex B2B work, the operating unit is account, buying group, problem, and trigger.

### 7.8 Stage 7: Behavioral Progression

Buyer progression uses six gates across the commercial and delivery journey:

```text
Problem Recognition
  -> Change Motivation
  -> Solution Confidence
  -> Decision Feasibility
  -> Commitment
  -> Realized Value
```

Each gate records the current buyer state, the constraint preventing movement, the intervention expected to cause movement, and the observed behavior that proves movement.

Seller activity is not progression. External buyer behavior controls the state transition.

The method-selection rule is:

- use Challenger when indifference or an unrecognized consequential gap prevents movement;
- use JOLT when the client wants change but decision uncertainty prevents movement; and
- use MEDDICC as the evidence layer for complex decision feasibility, not as a substitute for the selling method.

### 7.9 Stage 8: Revenue

Revenue requires buyer and seller commitment to the economic exchange. It establishes perceived value and creates a delivery obligation. It does not establish realized value.

### 7.10 Stage 9: Implementation

Implementation must establish the sequence:

```text
Purchase -> Setup -> Target Behavior -> First Value -> Repeated Value
```

The stage advances only on verified target behavior, not setup completion or internal delivery activity.

### 7.11 Stage 10: Value Realization

Verify three distinct levels:

1. usage: the client used the intervention;
2. behavior: the relevant human or operational behavior changed; and
3. outcome: that behavior produced the agreed desired client state.

The causal path is:

```text
Intervention -> Behavior Change -> Business Outcome -> Client Value
```

Compare the actual state with both the baseline and desired state using the measurement contract approved at Stage 0. Usage and behavior are not sufficient proxies for client value.

### 7.12 Stage 11: Retention and Expansion

Retention is the economic consequence of continued value exchange:

```text
Realized Value
  -> Continued Preference
  -> Renewal or Repeat Purchase
  -> Retained Revenue
```

Expansion starts from a newly observed consequential gap, not from an inventory of additional products. A new state can create new limitations and verified needs. Those observations return through Stage 0 revalidation to Stage 1 scouting.

## 8. Feedback loops

### 8.1 Revenue loop

```text
Problem -> Solution -> Demand -> Sale -> Revenue
```

### 8.2 Value loop

```text
Revenue -> Implementation -> Behavior -> Outcome -> Value -> Retention
```

### 8.3 Learning loop

```text
Observed Outcome
  -> Evidence
  -> Updated Beliefs
  -> Better Problem Selection
  -> Better Intervention
```

### 8.4 Compounding distribution loop

```text
Realized Value
  -> Retention
  -> Trust
  -> Evidence
  -> Reference or Referral
  -> Qualified Reach
```

## 9. Common operating record

Every active problem, opportunity, or client value cycle uses the same semantic fields:

| Field | Required question |
| --- | --- |
| Goal | What are we trying to accomplish? |
| Current State | What is true now? |
| Desired State | What must become true? |
| Gap | What separates the states? |
| Limitation | What evidence shows the current solution is insufficient? |
| Verified Need | What must change? |
| Target Behavior | What must somebody or some operation do differently? |
| Constraint | Why is that behavior not occurring? |
| Intervention | What should change the constraint? |
| Expected Effect | What should happen next? |
| Evidence | What would prove the effect occurred? |
| Buyer State | Which behavioral gate is active? |
| Economic State | What value is at stake? |
| Actual Outcome | What happened? |
| Value State | Was client value realized? |
| Retention State | Is continued exchange justified? |
| Learning | What changes in the operating model? |

These terms have one stable meaning across leadership, marketing, sales, product, operations, customer success, finance, and software delivery.

## 10. Measurement hierarchy

### 10.1 Controllable inputs

Measure interventions the organization can change, including ICP selection, problem hypothesis, channel, message, reframe, offer, recommendation, qualification threshold, implementation design, onboarding sequence, and service level.

### 10.2 Leading behavioral indicators

Measure evidence of state transition, including problem acknowledgment, economic-data disclosure, stakeholder introduction, decision-criteria confirmation, economic-buyer engagement, procurement activity, implementation-resource allocation, activation, target-behavior frequency, and outcome progress.

### 10.3 Economic outcomes

Measure qualified pipeline, win rate, sales-cycle time, revenue, gross profit, CAC, payback, churn, renewal, retained revenue, expansion, LTV, and net revenue retention.

A metric changing after an intervention does not by itself prove causality. The system must compare observed results with the approved expected effect and update beliefs using admitted evidence.

## 11. State-transition rule

No stage progresses because an internal task completed. A stage progresses only when its external exit condition becomes true and the state-transition service commits the qualified evidence.

Therefore:

- discovery-call completion is not problem recognition;
- proposal delivery is not solution confidence;
- demo completion is not decision feasibility;
- contract signature is not value realization;
- customer activity is not customer success; and
- a merged intervention is not realized client value.

## 12. Failure routes

- No verified problem: return evidence to scouting.
- Low consequence: stop pursuit.
- Poor ICP fit: disqualify.
- No solvable mechanism: do not build.
- Failed distribution economics: change the channel or market hypothesis.
- No change motivation: apply the admitted intervention or exit.
- High indecision: reduce decision uncertainty or stop forcing movement.
- Insufficient MEDDICC evidence: do not forecast the opportunity as committed.
- Failed implementation: return to diagnosis with evidence.
- Unrealized value: repair delivery before seeking expansion.
- Failed retention economics: repair the value system or intentionally close the relationship.

Failure is evidence. It must be returned to the applicable upstream stage.

## 13. Non-negotiable business invariants

1. Start every cycle with an approved goal, desired state, definition of done, objective function, and constraints.
2. Start commercial discovery with the client problem, not a preferred solution.
3. Treat pain as a state discrepancy, not an unverified complaint.
4. Validate that the problem is real, unsatisfied, consequential, reachable, and solvable before building or selling.
5. Define the target behavior required for the desired outcome.
6. Diagnose the constraint before selecting the intervention.
7. Optimize qualified reach, not raw reach.
8. Do not confuse seller activity with buyer progression.
9. Apply Challenger to indifference and JOLT to indecision.
10. Use MEDDICC as an evidence layer for complex decisions.
11. Revenue is not proof of realized value.
12. Verify the client state change against the original baseline and desired state.
13. Retained revenue requires continued value.
14. Return customer evidence to objective revalidation and problem scouting.
15. Use one stable meaning for state, gap, limitation, need, behavior, constraint, intervention, outcome, value, and retention.
16. Preserve human authority over consequential commitments and organizational change.

## 14. Software delivery boundary

The software factory is a subordinate intervention-delivery module:

```text
Scout -> Plan -> Build -> Test -> Review -> Lvvphole merge decision
```

Its terminal outputs are:

- `MERGE_READY`: bounded implementation with requirement traceability, qualified test evidence, independent review, and disclosed residual uncertainty;
- `DO_NOT_MERGE`: the candidate fails an acceptance or risk condition; or
- `BLOCKED`: required authority, evidence, capability, or dependency is unavailable.

Every repair loop is bounded by attempts, cost, elapsed time, and a measurable progress test. Repeated failure without new evidence terminates or escalates. Each repaired defect requires durable regression evidence.

The software factory cannot claim target behavior change, realized client value, retained revenue, or expansion. Those states require post-implementation evidence in Stages 9 through 11.
