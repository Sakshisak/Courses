BEGIN {
        session["Forenoonnull"] = "F";
        session["ForenoonAfternoon"] = "B";
        session["Afternoonnull"] = "A";
}
{
	centre=$2;
	FNB=$6 $10;
	if ((centre, FNB) in ids) {
	} else {
		ids[centre, FNB] = $1 "," $3 "," $9 "," $8 
	}
}	
END {
        print "0Session, centre, AppID, RollNo-1, RollNo-2, ZoneID";
	for (key in ids) {
		split(key,sep,SUBSEP);
		print session[sep[2]], ",", sep[1], "," ids[key];
	}
}
