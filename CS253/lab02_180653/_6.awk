BEGIN{FS=";"}
FNR>1{sum[$9]+=$2;
     count[$9]++;
     }
END{for (var in sum)
{ print var;
  print sum[var]/count[var];}
}
