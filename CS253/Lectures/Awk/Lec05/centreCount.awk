BEGIN {
        session["Forenoonnull"] = "F";
        session["ForenoonAfternoon"] = "B";
        session["Afternoonnull"] = "A";
}
{
	centre=$2;
	count[centre]++;
}
END {
        print "centre, count";
	for (key in count) {
		print key ", " count[key];
	}
}
