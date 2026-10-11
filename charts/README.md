# Chart provenance

`progress.png` and `progress.svg` are unchanged historical PR #3 assets from
head `9aecdfbd987ecda60b7c5e0b382849d67c6bbc2f`. Their final value 30 depended on
an unsupported transfer from the full-support DP to arbitrary active supports.
They are not current evidence and are no longer embedded in the progress page.

The corrected [progress table](../progress.md) records support-uniform 33 and
even dimension 34 for this residual step only. The original full-support DP's
ratio 28 remains unchanged and has a different scope.

`make_progress_chart.py` now generates `support33-progress.png` and
`support33-progress.svg` with value 34, preserving the historical images.
Run it only in an environment with matplotlib already available. No corrected
images were rendered or visually verified for this integration; matplotlib
was unavailable, and no packages were installed. External review of the
mathematical correction remains pending.
