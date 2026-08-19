# Security Authority

Load this file for identity, authority, capability, A2A, secret, sandbox, or external-effect work.

## Required controls

- Deny by default.
- The Authority Envelope is the sole organizational authority source.
- Effective authority is the intersection of the envelope, enterprise policy, task-required authority, receiver policy, and runtime constraints.
- A child grant must be a subset of the parent's effective grant.
- Prompts, memory, state projections, titles, tool visibility, SDK handoffs, and model output cannot grant authority.
- Privileged requests enter only through the Action Gate and `capabilityRuntime.invoke(...)`.
- Cross-sandbox communication uses authenticated, integrity-protected A2A envelopes and authorized source-to-receiver edges.
- Only ACTIVE principals can send, receive, or claim executable work.
- Each principal receives minimum-sufficient information, tools, budget, time, and filesystem access.
- Never commit credentials, tokens, private keys, customer data, internal endpoints, or secret values. Document only the approved retrieval mechanism.
- External effects require evidence beyond the tool response and the applicable independent verifier.

## Security result

Return `BLOCKED` when identity, authority, freshness, isolation, information scope, lease, or evidence cannot be established. Do not convert uncertainty into permission.
