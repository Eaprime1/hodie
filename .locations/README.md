# Location Configurations

Each location in the hodie ecosystem has unique hardware, paths, and roles.
Location configs are checked into git so any device can understand the network topology.
Local secrets/overrides go in `.env` (gitignored).

## Locations

| Name | Device | Role | ENV_NAME |
|------|--------|------|----------|
| mulberry | Laptop | HQ — primary dev, multi-stream orchestration | mulberry |
| pixel8a | Pixel 8a / Termux | Mobile — field capture, conversation processing | pixel8a |
| codespaces | GitHub Codespaces | Cloud — CI-adjacent work, ephemeral | codespaces |

## How It Works

1. `source .scripts/env_setup.sh` detects the current location
2. Location-specific config loads from `.locations/<name>/config.sh`
3. Scripts read `$LOCATION_NAME` and `$LOCATION_ROLE` to adapt behavior

## Adding a New Location

1. Create `.locations/<name>/config.sh` with exports
2. Add detection logic to `.scripts/env_setup.sh`
3. Document in this README
