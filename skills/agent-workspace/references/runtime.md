# Runtime Reference

Use this reference for runtime capability files, browser automation failures, sandbox limits, and local session profiles.

## Separation

Public runtime requirements describe what a task may need. They do not assert that the current machine or session has the capability.

Detected machine and session state belongs under ignored local state. Current session detection is more authoritative than cached machine state.

## Browser Automation

Do not treat browser automation failures as page assertion failures until the browser actually reaches the page.

For macOS sandbox failures such as Chromium `MachPortRendezvousServer Permission denied`, record the issue as a runtime environment limitation and route validation to an available surface such as controlled Chrome, host Terminal, or CI when the workspace policy allows it.

## Reporting

If validation cannot run on an available surface, report the validation gap explicitly. Do not mark UI validation complete based on code review alone.
