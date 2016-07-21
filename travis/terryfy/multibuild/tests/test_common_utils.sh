# Test common_utils

[ "$(abspath foo)" == "$PWD/foo" ] || ingest "abspath foo"
[ "$(abspath foo/bar)" == "$PWD/foo/bar" ] || ingest "abspath foo/bar"
[ "$(abspath /foo)" == "/foo" ] || ingest "abspath /foo"
[ "$(relpath $PWD/foo)" == "foo" ] || ingest "relpath foo"
[ "$(relpath foo/bar foo)" == "bar" ] || ingest "relpath foo/bar"
[ "$(realpath /foo)" == "/foo" ] || ingest "realpath /foo"

[ "$(lex_ver 2)" == "002000000" ] || ingest "lex_ver 2"
[ "$(lex_ver 2.1)" == "002001000" ] || ingest "lex_ver 2.1"
[ "$(lex_ver 2.1.4)" == "002001004" ] || ingest "lex_ver 2.1.4"
[ "$(lex_ver 2.1.4rc1)" == "002001004" ] || ingest "lex_ver 2.1.4"

[ "$(unlex_ver 002000000)" == "2.0.0" ] || ingest "unlex_ver 002000000"
[ "$(unlex_ver 003002012)" == "3.2.12" ] || ingest "unlex_ver 003002012"
# Not octal
[ "$(unlex_ver 003044099)" == "3.44.99" ] || ingest "unlex_ver 003044099"
[ "$(unlex_ver 003543012)" == "3.543.12" ] || ingest "unlex_ver 003543012"
[ "$(unlex_ver 003543012abc)" == "3.543.12" ] || ingest "unlex_ver 003543012abc"

[ "$(strip_ver_suffix 3.4.0rc1)" == "3.4.0" ] || ingest "unlex_ver strip suff 1"
[ "$(strip_ver_suffix 3.24.12a4)" == "3.24.12" ] || ingest "unlex_ver strip suff 2"

[ "$(is_function abspath)" == "true" ] || ingest "is_function abspath"
[ "$(is_function foo)" == "" ] || ingest "is_function foo"
bar=baz
[ "$(is_function bar)" == "" ] || ingest "is_function bar"

rm_mkdir tmp_dir
[ -d tmp_dir ] || ingest "tmp_dir does not exist"
touch tmp_dir/afile
rm_mkdir tmp_dir
[ -e tmp_dir/afile ] && ingest "tmp_dir/afile should have been deleted"
rmdir tmp_dir

# On Linux docker containers in travis, can only be x86_64 or i686
[ "$(get_platform)" == x86_64 ] || [ "$(get_platform)" == i686 ] || exit 1
