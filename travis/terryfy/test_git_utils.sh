# Check git commit utilities
# Check commit finding
# Clean any old repos from previous test run
REPO_ROOT=repo-testing
REPO_SDIR=a_repo

rm -rf $REPO_ROOT

# Make new test repo
mkdir $REPO_ROOT
cd $REPO_ROOT
mkdir $REPO_SDIR
cd $REPO_SDIR
git init
git commit --allow-empty -m 'initial'
FIRST=$(git rev-parse HEAD)
git branch first-branch
git checkout first-branch
git commit --allow-empty -m 'filler-commit'
FILLER=$(git rev-parse HEAD)
git commit --allow-empty -m 'on-first-branch-1'
git tag off-first -m 'off-first'
OFF_FIRST=$(git rev-parse HEAD)
git commit --allow-empty -m 'on-first-branch-2'
AFTER_OFF_FIRST=$(git rev-parse HEAD)
git checkout master
git commit --allow-empty -m 'second'
git tag second -m 'second tag'
SECOND=$(git rev-parse HEAD)
git commit --allow-empty -m 'third'
THIRD=$(git rev-parse HEAD)
MASTER=$THIRD
# Make a branch off the first commit
git branch other $FIRST
git checkout other
git commit --allow-empty -m 'other-second'
# This is to check tag directly branched off history
OTHER=`git rev-parse HEAD`
git checkout $OTHER
git commit --allow-empty -m 'off other 1'
git commit --allow-empty -m 'off other 2'
git tag early-tag -m 'early-tag'
EARLY_TAG=`git rev-parse HEAD`
# Push everything up to backup repo
git init --bare ../b_repo.git
git remote add origin ../b_repo.git
git push --all origin
cd ..

function check_hash {
    cd $REPO_SDIR
    actual_commit=`git rev-parse HEAD`
    if [[ $actual_commit != $1 ]]; then
        echo "$actual_commit != $1"
        RET=1
    fi
    cd ..
}

# Checkout commit hash
checkout_commit $REPO_SDIR $SECOND
check_hash $SECOND
# Checkout default (master)
checkout_commit $REPO_SDIR
check_hash $MASTER
# Checkout non-default branch
checkout_commit $REPO_SDIR other
check_hash $OTHER
# Checkout a tag name
checkout_commit $REPO_SDIR second
check_hash $SECOND
# Checkout latest tag on default branch (master)
checkout_commit $REPO_SDIR $OTHER  # go somewhere else first
checkout_commit $REPO_SDIR latest-tag
check_hash $SECOND
# Check other branch, and tag direct extension from branch
checkout_commit $REPO_SDIR latest-tag other
check_hash $EARLY_TAG
# Check earlier commit hash for tag source
checkout_commit $REPO_SDIR latest-tag $SECOND
check_hash $SECOND
checkout_commit $REPO_SDIR latest-tag first-branch
check_hash $OFF_FIRST
checkout_commit $REPO_SDIR latest-tag $FILLER
check_hash $OFF_FIRST
# Add an extra tag to early branch
cd $REPO_SDIR
git tag after-off-first -am "Message" $AFTER_OFF_FIRST
cd ..
# Check we get the second of the two tags now
checkout_commit $REPO_SDIR
checkout_commit $REPO_SDIR latest-tag $FILLER
check_hash $AFTER_OFF_FIRST

# Clean up after
cd ..
rm -rf $REPO_ROOT
