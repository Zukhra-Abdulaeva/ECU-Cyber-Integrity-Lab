# ECU / Security Domain Model

## 1. Project Identity

Project: ECU-Cyber-Integrity-Lab  
ECU / SECURITY DOMAIN MODEL

The model establishes the ECU-oriented security context supported by the current project information. It does not establish implementation, execution, evidence or security findings.

## 2. Model Status

| Status | Meaning |
|---|---|
| ESTABLISHED | Directly supported by current project documentation or repository content |
| CONTEXTUAL | Project context, but not a concrete current implementation element |
| INFERRED | Explicitly derived inference; not a project fact |
| UNKNOWN | Required information is unavailable |
| NOT ESTABLISHED | Relevant, but insufficiently established |

## 3. ECU / Component Inventory

| ID | Element | Type | Technical role | Domain | Interface | Assets | Security properties | Status | Basis |
|---|---|---|---|---|---|---|---|---|---|
| ECU-01 | Gateway ECU | ECU category | Gateway / communication routing; firmware-bearing context | CAN; wider vehicle context | CAN; firmware artifact | Firmware; CAN communication | Integrity; Communication security; Firmware integrity | CONTEXTUAL | Project automotive context; current terminology |
| ECU-02 | ECU-oriented diagnostic function | ECU-oriented function | Diagnostic communication | UDS over CAN | Diagnostic request / response | Diagnostic services | Diagnostic security; Access control; Communication security | CONTEXTUAL | UDS implementation and project context |
| ECU-03 | ECU-oriented firmware-bearing component | ECU-oriented component | Firmware-bearing function | Not established | Firmware artifact | Firmware; ECU software | Integrity; Firmware integrity; Authenticity | NOT ESTABLISHED | Firmware implementation and project context |

No concrete physical ECU instance is established for these elements.

## 4. Communication Domains

| ID | Domain | Technical role | Connected elements | Status | Basis |
|---|---|---|---|---|---|
| CD-01 | CAN | Communication technology / network domain | ECU-01; ECU-02 | ESTABLISHED | CAN implementation |
| CD-02 | UDS over CAN | Diagnostic protocol / service domain | ECU-02; diagnostic services | ESTABLISHED | UDS implementation uses Python CAN / SocketCAN |
| CD-03 | Ethernet / IP networking | Network communication domain | Network-oriented context | ESTABLISHED | Ethernet/IP scanning implementation |
| CD-04 | Automotive Ethernet | Automotive network context | Network-oriented context | CONTEXTUAL | Project automotive context |
| CD-05 | CAN FD / LIN / FlexRay | Vehicle-network context | Not established | CONTEXTUAL | Project context |

Technology and diagnostic/application domains remain distinct.

## 5. Interface Inventory

| ID | Interface | Connected element(s) | Domain | Function | Assets | Security relevance | Status | Basis |
|---|---|---|---|---|---|---|---|---|
| IF-01 | CAN / SocketCAN | ECU-01; ECU-02 | CAN | CAN traffic capture/generation and diagnostic communication | CAN communication; diagnostic services | Communication security; Availability | ESTABLISHED | CAN/UDS implementation; `vcan0` |
| IF-02 | Diagnostic request / response | ECU-02 | UDS over CAN | UDS request/response handling | Diagnostic services | Diagnostic security; Access control; Communication security | ESTABLISHED | UDS implementation |
| IF-03 | IP network interface | Network-oriented context | Ethernet / IP | Host/service discovery and port scanning | Network interfaces | Communication security; Availability | ESTABLISHED | Ethernet implementation |
| IF-04 | Network service interface | Network-oriented context | Ethernet / IP | Network service exposure context | Network services | Availability; Access control; Communication security | NOT ESTABLISHED | Service/port references exist; target relationship unresolved |
| IF-05 | Firmware artifact interface | ECU-03 context | Firmware | Firmware input, hashing and comparison | Firmware; ECU software | Integrity; Firmware integrity; Authenticity | ESTABLISHED | Firmware implementation |

## 6. Asset Model

| ID | Asset | Type | Associated element | Domain | Interface | Security property | Status | Basis |
|---|---|---|---|---|---|---|---|---|
| AS-01 | ECU software | Software asset | ECU-03 context | Not established | IF-05 | Integrity; Authenticity | CONTEXTUAL | Project asset context |
| AS-02 | Firmware | Firmware artifact | ECU-01 / ECU-03 context | Not established | IF-05 | Integrity; Firmware integrity; Authenticity | ESTABLISHED | Firmware implementation; referenced firmware artifacts |
| AS-03 | CAN communication | Communication asset | ECU-01; ECU-02 | CD-01 | IF-01 | Communication security; Availability | ESTABLISHED | CAN implementation |
| AS-04 | Diagnostic services | Diagnostic asset | ECU-02 | CD-02 | IF-02 | Diagnostic security; Access control; Communication security | ESTABLISHED | UDS implementation |
| AS-05 | Network interfaces | Network asset | Network-oriented context | CD-03 | IF-03 | Communication security; Availability | ESTABLISHED | Ethernet/IP implementation |
| AS-06 | Automotive-oriented network services | Network/service asset | Network-oriented context | CD-03 / CD-04 | IF-04 | Availability; Access control; Communication security | NOT ESTABLISHED | Service/port references; concrete target unresolved |
| AS-07 | Vehicle communication paths | Communication-path asset | ECU-oriented context | Not established | Not established | Communication security; Availability | NOT ESTABLISHED | Phase-2 scope; no concrete project-wide path established |

## 7. Security Property Mapping

| ID | Element | Property | Basis | Status |
|---|---|---|---|---|
| SP-01 | AS-02 Firmware | Integrity | SHA-256 hashing and integrity checking are implemented | ESTABLISHED |
| SP-02 | AS-02 Firmware | Firmware integrity | Explicit project security area and implementation capability | ESTABLISHED |
| SP-03 | AS-02 Firmware | Authenticity | Security-property context; no authenticity mechanism established | CONTEXTUAL |
| SP-04 | AS-03 CAN communication | Communication security | Established security-assessment and communication domain | ESTABLISHED |
| SP-05 | AS-03 CAN communication | Availability | Relevant to communication asset; no protection verification | CONTEXTUAL |
| SP-06 | AS-04 Diagnostic services | Diagnostic security | UDS and SecurityAccess handling implemented | ESTABLISHED |
| SP-07 | AS-04 Diagnostic services | Access control | SecurityAccess is an implemented diagnostic function | ESTABLISHED |
| SP-08 | AS-04 Diagnostic services | Communication security | Diagnostic communication established over CAN | ESTABLISHED |
| SP-09 | AS-05 Network interfaces | Communication security | IP/network communication is an established assessment area | ESTABLISHED |
| SP-10 | AS-05 Network interfaces | Availability | Relevant network property; no control verification | CONTEXTUAL |
| SP-11 | AS-01 ECU software | Integrity | Asset is documented; concrete control relationship incomplete | CONTEXTUAL |
| SP-12 | AS-06 Network services | Access control | Relevant in context; concrete service/control relationship unresolved | NOT ESTABLISHED |

Confidentiality is not assigned to a specific model element because the available project information does not establish a sufficiently specific relationship.

## 8. Security-Domain Relationship Matrix

| ID | ECU / Component | Domain | Interface | Asset | Property | Security domain | Status |
|---|---|---|---|---|---|---|---|
| R-01 | ECU-01 | CD-01 CAN | IF-01 | AS-03 | Communication security | CAN Security | ESTABLISHED |
| R-02 | ECU-02 | CD-02 UDS | IF-02 | AS-04 | Diagnostic security | UDS Diagnostic Security | ESTABLISHED |
| R-03 | ECU-02 | CD-02 UDS | IF-01 | AS-03 | Communication security | UDS Diagnostic Security | ESTABLISHED |
| R-04 | ECU-01 / ECU-03 context | — | IF-05 | AS-02 | Integrity; Firmware integrity | Firmware Security | ESTABLISHED |
| R-05 | Network-oriented context | CD-03 Ethernet/IP | IF-03 | AS-05 | Communication security | Automotive Ethernet Security | ESTABLISHED |
| R-06 | Network-oriented context | CD-03 Ethernet/IP | IF-04 | AS-06 | Availability; Access control | Automotive Ethernet Security | NOT ESTABLISHED |
| R-07 | ECU-01 context | CD-01 CAN | IF-01 | AS-03 | Availability | CAN Security | CONTEXTUAL |
| R-08 | ECU-03 context | — | IF-05 | AS-01 | Integrity | Firmware Security | CONTEXTUAL |

## 9. Security-Domain Boundaries

| ID | Boundary | Technical basis | Status |
|---|---|---|---|
| B-01 | CAN communication / UDS diagnostic service | UDS request/response is implemented using CAN / SocketCAN | ESTABLISHED |
| B-02 | IP network interface / network service layer | Ethernet implementation performs host and service discovery | ESTABLISHED |
| B-03 | Firmware artifact / firmware-bearing context | Firmware is processed as an artifact associated with firmware context | ESTABLISHED |
| B-04 | Vehicle communication path / concrete project implementation | No concrete project-wide physical path established | NOT ESTABLISHED |

These are technical boundaries. No trust relationship is inferred from a communication connection.

## 10. Assessment-Surface Mapping

| Surface | Model connection | Status | Basis |
|---|---|---|---|
| CAN communication | CD-01 / IF-01 / AS-03 | ESTABLISHED | CAN implementation |
| UDS diagnostics | CD-02 / IF-02 / AS-04 | ESTABLISHED | UDS implementation |
| IP-based network services | CD-03 / IF-03 / IF-04 / AS-05 / AS-06 | ESTABLISHED at model level; target unresolved | Ethernet/IP implementation and current state |
| Firmware artifacts | IF-05 / AS-02 | ESTABLISHED | Firmware implementation |

The mapping is structural and does not represent an executed attack or confirmed vulnerability.

## 11. Traceability

| Element | Basis | Security domain | State |
|---|---|---|---|
| ECU-01 | Project automotive context | CAN / Firmware | CONTEXTUAL |
| ECU-02 | UDS implementation | UDS Diagnostic Security | CONTEXTUAL |
| ECU-03 | Firmware implementation/context | Firmware Security | NOT ESTABLISHED |
| CD-01 | CAN implementation | CAN Security | ESTABLISHED |
| CD-02 | UDS implementation | UDS Diagnostic Security | ESTABLISHED |
| CD-03 | Ethernet/IP implementation | Automotive Ethernet Security | ESTABLISHED |
| IF-01 | CAN/UDS implementation | CAN / UDS | ESTABLISHED |
| IF-02 | UDS implementation | UDS | ESTABLISHED |
| IF-03 | Ethernet implementation | Ethernet/IP | ESTABLISHED |
| IF-04 | Service/port references | Ethernet/IP | NOT ESTABLISHED |
| IF-05 | Firmware implementation | Firmware Security | ESTABLISHED |
| AS-02 | Firmware implementation/artifacts | Firmware Security | ESTABLISHED |
| AS-03 | CAN implementation | CAN Security | ESTABLISHED |
| AS-04 | UDS implementation | UDS Diagnostic Security | ESTABLISHED |
| AS-05 | Ethernet/IP implementation | Automotive Ethernet Security | ESTABLISHED |
| AS-06 | Context/service references | Automotive Ethernet Security | NOT ESTABLISHED |
| AS-07 | Phase-2 scope context | Multiple | NOT ESTABLISHED |

## 12. Known Gaps

- Concrete physical ECU instances
- Concrete ECU-to-ECU topology
- Concrete vehicle communication paths
- Concrete Ethernet target
- Concrete ownership of network services
- Complete project-wide asset inventory
- Complete project-wide security-property model
- Unified attacker-capability model
- Concrete trust relationships

The gaps are explicitly classified and are not completed from generic automotive assumptions.

## 13. State Separation

| State | Phase-2 result |
|---|---|
| Model | ESTABLISHED |
| New implementation | NONE |
| Phase-2 security-test execution | NOT PERFORMED |
| New Phase-2 execution evidence | NONE |
| Security findings | NONE ESTABLISHED |
| Model-level verification | PERFORMED |
| Security-control verification | NOT PERFORMED |

## 14. Artefact Coverage

| Artefact | Result |
|---|---|
| A1 ECU / Security Domain Model | ESTABLISHED |
| A2 ECU and Component Inventory | ESTABLISHED |
| A3 Communication Domain Inventory | ESTABLISHED |
| A4 Interface Inventory | ESTABLISHED |
| A5 Asset Model | ESTABLISHED |
| A6 Security Property Mapping | ESTABLISHED |
| A7 Security-Domain Relationship Matrix | ESTABLISHED |
| A8 Model Traceability Record | ESTABLISHED |
| A9 Phase-2 Current-State Update | PROVIDED |
| A10 Phase-2 Review Record | ESTABLISHED |

## 15. Verification Results

| Criterion | Result |
|---|---|
| VC-01 ECU Model | PASS |
| VC-02 Communication Domains | PASS |
| VC-03 Interfaces | PASS |
| VC-04 Asset Inventory | PASS |
| VC-05 Security Property Mapping | PASS |
| VC-06 Domain Relationships | PASS |
| VC-07 Security-Domain Boundaries | PASS |
| VC-08 Attack-Surface Connection | PASS |
| VC-09 Traceability | PASS |
| VC-10 Status Integrity | PASS |
| VC-11 Implementation Separation | PASS |
| VC-12 Current-State Synchronization | PASS |
| VC-13 Phase Scope | PASS |

These are model-review results, not security-test execution results.

## 16. Completion Gate

| Condition | Result |
|---|---|
| ECU / Security Domain Model | ESTABLISHED |
| ECU / Component Inventory | ESTABLISHED |
| Communication Domain Inventory | ESTABLISHED |
| Interface Inventory | ESTABLISHED |
| Asset Model | ESTABLISHED |
| Security Property Mapping | ESTABLISHED |
| Security-Domain Relationships | ESTABLISHED |
| Relevant Security-Domain Boundaries | DOCUMENTED |
| Assessment-Surface Relationships | DOCUMENTED WHERE ESTABLISHED |
| Model Traceability | ESTABLISHED |
| Unresolved Model Elements | EXPLICITLY CLASSIFIED |
| Verification Criteria | REVIEWED |
| Current State | SYNCHRONIZED IN PROVIDED UPDATE |
