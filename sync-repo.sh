#!/bin/bash
# Copies everything shareable from ~/gradeo into the repo ~/hsc-se-study (public until after the HSC; the user
# chose to include trial papers and the question bank). Large videos are not copied: the repo keeps re-encoded
# copies (GitHub's 100 MB file limit).
set -e
R=~/hsc-se-study
cd ~/gradeo
X=(--exclude .DS_Store --exclude __pycache__ --exclude node_modules --exclude .venv)
rsync -a --delete "${X[@]}" --exclude export.mjs exam-app/ "$R/exam-app/"
rsync -a "${X[@]}" papers/ "$R/papers/"
rsync -a "${X[@]}" private_papers/ "$R/private_papers/"
rsync -a "${X[@]}" --exclude '*.mp4' --exclude '*.mov' question_bank/ "$R/question_bank/"
rsync -a "${X[@]}" study/ "$R/study/"
rsync -a "${X[@]}" practice/ "$R/practice/"
rsync -a "${X[@]}" discord_inbox/ "$R/discord_inbox/"
cp REVISION.md syllabus-tracker.md sync-repo.sh import_private.mjs build.mjs fetch.mjs lib.mjs bridge.mjs connect.mjs render_drawings.mjs "$R/"
echo "synced; now: cd $R && git add -A && git commit && git push"
