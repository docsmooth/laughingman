# AGENTS.md - working agreement for this repo

## Project

This repository contains a Pebble watch app/watchface built with the
current RePebble SDK.

Development is done primarily from Ubuntu under WSL on Windows using
VS Code and GitHub Copilot.

Treat the source tree and package.json as the as-built truth. Do not
assume APIs, platforms, dependencies, or SDK behavior from historical
Pebble knowledge.

## Pebble documentation

The authoritative SDK documentation is:

https://developer.repebble.com/

Documentation index for coding agents:

https://developer.repebble.com/llms.txt

Before using or changing a Pebble API, consult the current RePebble
documentation.

Most documentation pages have a Markdown version. Replace the trailing
"/" or "/index.html" with ".md".

Examples:

https://developer.repebble.com/guides/events-and-services/buttons.md
https://developer.repebble.com/docs/c/llms-full.txt

For API lookup, use:

https://developer.repebble.com/api-index.json

Prefer those sources over remembered or historical Pebble SDK behavior.

If documentation and existing code disagree, identify the discrepancy
rather than silently rewriting working code.

## SDK and environment

Development environment:

- Ubuntu under WSL
- current `pebble-tool`
- SDK installed through `pebble sdk`
- build and emulator operations run inside WSL

The Pebble CLI is installed with:

    uv tool install pebble-tool

Inspect the installed SDK rather than assuming its version:

    pebble sdk list

The current RePebble documentation describes SDK 4.33.1, but the locally
installed SDK is authoritative for the build environment.

Important: `sdkVersion` in package.json remains `"3"` even for
applications built using SDK 4.x. Do not "fix" it based solely on the
installed SDK version.

## Target platforms

Read `targetPlatforms` from package.json before changing
platform-dependent code.

Current Pebble platform identifiers are:

- aplite
- basalt
- chalk
- diorite
- emery
- flint
- gabbro

Do not assume screen dimensions, color capabilities, input hardware,
or API availability across platforms. Check the Hardware Information
and API documentation first.

Alloy projects support only emery and gabbro. Projects targeting older
Pebble hardware must use C.

## Build verification

After changing application code, build the project:

    pebble build

A successful compile is the minimum verification bar.

Do not report a code change as working merely because the source looks
correct.

When practical, test it in the emulator as well.

Default emulator target unless package.json or the task says otherwise:

    emery

Install:

    pebble install --emulator emery

Capture the screen:

    pebble screenshot --no-open --emulator emery screenshot.png

Inspect application logs:

    pebble logs --emulator emery

Interact with the emulator when necessary:

    pebble emu-button click back --emulator emery
    pebble emu-button click up --emulator emery
    pebble emu-button click select --emulator emery
    pebble emu-button click down --emulator emery

For environments without a graphical display, use `--vnc` with
emulator commands.

If the emulator behaves inconsistently:

    pebble kill
    pebble wipe

Then reinstall the application.

## Verification workflow

For a normal code change:

1. Read the relevant existing code.
2. Check package.json for project type and target platforms.
3. Look up unfamiliar Pebble APIs in the current RePebble docs.
4. Make the smallest change that satisfies the request.
5. Run `pebble build`.
6. If visual or runtime behavior changed, install in an appropriate emulator.
7. Capture a screenshot when UI appearance matters.
8. Check `pebble logs` when runtime behavior matters.
9. Report what was verified versus what was only inferred.

Do not hide compiler warnings or emulator/runtime errors.

## Coding guidance

Prefer existing project conventions over introducing new patterns.

Keep changes scoped to the requested behavior.

Before introducing a new Pebble API:
- confirm that it exists in the current documentation;
- verify that it is available on this project's target platforms;
- follow the documented lifetime and callback rules;
- check return values and failure cases where applicable.

Do not invent Pebble APIs from memory.

Be especially cautious with old Pebble examples found elsewhere on the
Internet. Pebble has existed through multiple SDK generations and much
historical documentation remains searchable.

Current developer.repebble.com documentation takes precedence.

## Resources and package.json

Treat package.json as project configuration, not disposable generated
content.

Before modifying:
- targetPlatforms
- capabilities
- resources
- message keys
- app/watchface metadata

read the corresponding current RePebble documentation.

Do not remove an existing platform merely to make a build pass unless
the requested change explicitly changes supported hardware.

## Physical watch installation

Do not assume that a physical watch is available.

When physical-device testing is explicitly requested, supported
connection methods include the RePebble CloudPebble developer connection
and a LAN developer connection.

CloudPebble installation uses:

    pebble login
    pebble install --cloudpebble

Do not change persistent login or connection configuration unless asked.

## Git discipline

Before editing, inspect:

    git status
    git diff

Do not overwrite unrelated local changes.

Keep generated emulator screenshots, temporary build artifacts, and
debug output out of the repository unless they are intentionally part
of the project.

Do not commit, push, create a tag, or publish the Pebble application
unless explicitly asked.

## AI-agent rule

Never rely on model memory for a Pebble API when the documentation can
answer the question.

Start at:

https://developer.repebble.com/llms.txt

Then fetch the `.md` version of the relevant documentation page before
implementing an unfamiliar API.

Use:

https://developer.repebble.com/api-index.json

when looking for a specific C or PebbleKit JS symbol.

Distinguish clearly between:

- VERIFIED - confirmed by documentation, build, emulator, or device
- INFERRED - concluded from existing code but not runtime tested
- RECOMMENDED - a proposed change not yet implemented or tested

When reporting completed work, state which verification was actually
performed.