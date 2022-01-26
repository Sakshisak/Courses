BEGIN{FS=";"}
FNR>1{arr[$9,1] += $2;
	arr[$9,2]++; 
     }
END{for (var in arr)
{ print var;
  split(var,sep, SUBSEP);
  print sep[1]," , ", sep[2];
  print arr[var,1]/arr[var,2];}
}
