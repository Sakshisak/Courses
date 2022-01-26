#include <stdio.h>

int fib(int a , int b)
{
    if (a <= 0 && b<= 0)
    return 0;
    else if (a >= 0 && b<= 0)
    return a;
    else if (a <= 0 && b>= 0)
    return b;
    int carry = (a & b) << 1 ;
    int sum = (a ^ b);
    return fib(carry, sum);
}
int fib2(int a, int b)
{
    while(a!=0)
    {
     int carry = b&a;
     b=b^a;
    a=carry<<1;
    }
    return b;
}
int static count = 0;


int main(){
    // printf("Enter your name:\n");
    // char str[50];
    // scanf("%s",str);
    // printf("Your name is : Sakshi\n");

    // printf("%d\n",fib(3,2));
    // printf("%d\n",fib2(3,2));



    // while(1){
    //     printf("%d\n",count++);
    //     if(count > 10000000)
    //         break;
    // }
    printf("Bitwise or: %d \n",5 | 5);

    return 0;

}
