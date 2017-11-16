#include <stdio.h>
#include <unistd.h>
#include <errno.h>

#define  CString char*

void ReadDxf(FILE *fp)  
{  
      
    bool entities=false;//标识是否进入实体区间  
    CString str,str2;//临时的字符变量  
    float x,y,z;//x,y,z坐标  
    int LayerIndex=-1;  
    CString LayerName;//文件名  
    int n=0;  
    int flag=0;  
    while(!feof(fp)&&!ferror(fp))  
    {  
        pFrm->SetPos(ftell(fp)/1024);//显示进度，占用时间，去掉此句可以加快读取速度  
        fscanf(fp,"%s\n",str);  
        if(strcmp(str,"ENTITIES")==0) entities=true;//判断是否进入实体区间  
        if(strcmp(str,"ENDSEC")==0&&entities) {entities=false;break;}//是否已经读到实体区间外  
          
        if(strcmp(str,"POINT")==0&&entities)//在实体区间中读到点标志  
        {  
            while(strcmp(str,"8")!=0){//"POINT"之后肯定有"8"标志  
                fscanf(fp,"%s\n",str);  
            }  
            fscanf(fp,"%s\n",LayerName);//"8"标志后跟的是层名，表明这个点属于这个层  
            while(strcmp(str,"10")!=0){//之后会有"10"标志出现  
                fscanf(fp,"%s\n",str);  
            }  
            fscanf(fp,"%f\n",&x);//"10"表示后面跟的数据是此点的X坐标  
            fscanf(fp,"%*s\n");//"11"  
            fscanf(fp,"%f\n",&y);//"11"表示后面跟的数据是此点的Y坐标  
            fscanf(fp,"%*s\n");//"12"  
            fscanf(fp,"%f\n",&z);//"12"表示后面跟的数据是此点的Z坐标  
        }  
        ///////////////////  
        if(strcmp(str,"LINE")==0&&entities)//在实体区间中读到线段标志  
        {  
            while(strcmp(str,"8")!=0){  
                fscanf(fp,"%s\n",str);  
            }  
            fscanf(fp,"%s\n",LayerName);//LayerName  
            while(strcmp(str,"10")!=0){  
                fscanf(fp,"%s\n",str);  
            }  
            fscanf(fp,"%f\n",&x);//线段第一个点的3维坐标  
            fscanf(fp,"%*s\n");  
            fscanf(fp,"%f\n",&y);  
            fscanf(fp,"%*s\n");  
            fscanf(fp,"%f\n",&z);  
            fscanf(fp,"%*s\n");  
            fscanf(fp,"%f\n",&x);//线段第二个点的3维坐标  
            fscanf(fp,"%*s\n");  
            fscanf(fp,"%f\n",&y);  
            fscanf(fp,"%*s\n");  
            fscanf(fp,"%f\n",&z);  
        }  
        ///////////////////  
        if(strcmp(str,"LWPOLYLINE")==0&&entities)//在实体区间中读到连续线段标志  
        {  
            CPloyLine* pPloyLine=new CPloyLine();  
            while(strcmp(str,"8")!=0){  
                fscanf(fp,"%s\n",str);  
            }  
            fscanf(fp,"%s\n",LayerName);//LayerName  
            while(strcmp(str,"90")!=0){//"90"后跟的是此连续线段有多少个点  
                fscanf(fp,"%s\n",str);  
            }  
            fscanf(fp,"%d\n",&n);//点数  
            fscanf(fp,"%*s\n");//紧跟的是"70"标志,表示此曲线是否是封闭曲线  
            fscanf(fp,"%d\n",&flag);//0则不封闭，1则封闭。  
            fscanf(fp,"%*s\n");//43  
            fscanf(fp,"%*s\n");//0.0  
            fscanf(fp,"%s\n",str);  
            z=0.0;  
            if(strcmp(str,"38")==0){//此连续线段有着同样的Z坐标  
                fscanf(fp,"%f\n",&z);//z值  
                fscanf(fp,"%*s");  
            }  
            for(int i=0;i<n;i++)//按上面得到的总点数循环读取点坐标,此循环内无Z值  
            {  
                fscanf(fp,"%f\n",&x);  
                fscanf(fp,"%*s\n");  
                fscanf(fp,"%f\n",&y);  
                fscanf(fp,"%*s\n");  
            }  
        }  
        ///////////////////  
        if(strcmp(str,"CIRCLE")==0&&entities)//在实体区间中读到圆标志  
        {  
            while(strcmp(str,"8")!=0){  
                fscanf(fp,"%s\n",str);  
            }  
            fscanf(fp,"%s\n",LayerName);//LayerName  
            while(strcmp(str,"10")!=0){  
                fscanf(fp,"%s\n",str);  
            }  
            fscanf(fp,"%f\n",&x);//圆的圆心坐标  
            fscanf(fp,"%*s\n");  
            fscanf(fp,"%f\n",&y);  
            fscanf(fp,"%*s\n");  
            fscanf(fp,"%f\n",&z);  
            fscanf(fp,"%*s\n");  
            fscanf(fp,"%f\n",&x);//圆的半径  
        }  
        /////////////////////////////////---ARC---  
        if(strcmp(str,"ARC")==0&&entities)//在实体区间中读到圆弧标志  
        {  
            while(strcmp(str,"8")!=0){  
                fscanf(fp,"%s\n",str);  
            }  
            fscanf(fp,"%s\n",LayerName);//LayerName  
            while(strcmp(str,"10")!=0){  
                fscanf(fp,"%s\n",str);  
            }  
            fscanf(fp,"%f\n",&x);//圆弧的圆心坐标  
            fscanf(fp,"%*s\n");  
            fscanf(fp,"%f\n",&y);  
            fscanf(fp,"%*s\n");  
            fscanf(fp,"%f\n",&z);  
            fscanf(fp,"%*s\n");  
            fscanf(fp,"%f\n",&x);  
            while(strcmp(str,"50")!=0){  
                fscanf(fp,"%s\n",str);  
            }  
            fscanf(fp,"%f\n",&y);//圆弧的起始角  
            fscanf(fp,"%*s\n");  
            fscanf(fp,"%f\n",&z);//圆弧的终止角  
        }  
        ///---3DFACE---重要元素!--3维图形在AutoCAD中被炸开后都炸成一片一片的3DFACE---////////  
        if(strcmp(str,"3DFACE")==0&&entities)//在实体区间中读到3维面标志,4个点组成,但通常第4个点和第3个点重合,根据标志位判断  
        {  
            while(strcmp(str,"8")!=0){  
                fscanf(fp,"%s\n",str);  
            }  
            fscanf(fp,"%s\n",LayerName);//LayerName  
            while(strcmp(str,"10")!=0){//点坐标总是以'10'标志开始,  
                fscanf(fp,"%s\n",str);  
            }  
            fscanf(fp,"%f\n",&x);//第一个点  
            fscanf(fp,"%*s\n");//20  
            fscanf(fp,"%f\n",&y);//y  
            fscanf(fp,"%*s\n");  
            fscanf(fp,"%f\n",&z);//z  
              
            fscanf(fp,"%*s\n");  
            fscanf(fp,"%f\n",&x);//第二个点  
            fscanf(fp,"%*s\n");  
            fscanf(fp,"%f\n",&y);  
            fscanf(fp,"%*s\n");  
            fscanf(fp,"%f\n",&z);  
              
            fscanf(fp,"%*s\n");  
            fscanf(fp,"%f\n",&x);//第三个点  
            fscanf(fp,"%*s\n");  
            fscanf(fp,"%f\n",&y);  
            fscanf(fp,"%*s\n");  
            fscanf(fp,"%f\n",&z);  
            fscanf(fp,"%s\n",str2);  
            if(strcmp(str2,"13")==0)//如果在读完3个点后,紧跟的后面读到'13'标志,说明存在不同于第3个点的第4个点  
            {  
                fscanf(fp,"%f\n",&x);  
                fscanf(fp,"%*s\n");  
                fscanf(fp,"%f\n",&y);  
                fscanf(fp,"%*s\n");  
                fscanf(fp,"%f\n",&z);  
                fscanf(fp,"%s\n",str2);  
                if(strcmp(str2,"70")==0)//读取边的显示标志,这个标志很重要,标志着哪些边是需要显示的.  
                {  
                    fscanf(fp,"%d\n",&flag);  
                      
                }     
            }  
            else if(strcmp(str2,"70")==0)//如果在读完3个点后,紧跟的后面读到'70'标志,表示后面跟的是边的显示标志,并且说明第4个点与第3个点相同  
            {  
                  
                fscanf(fp,"%d\n",&flag);  
                  
            }  
            if(flag!=15)//即有可见边。如果==15,表示此3维面不需要显示出来.  
            {  
                  
            }  
            else//没有可见边则删除，不添加到列表。  
              
        }     
        ///--POLYLINE--更关键的元素--使得3维图形不需要炸开都能读取--它有3种不同的形态//////////////////////////  
        if(strcmp(str,"POLYLINE")==0 && entities)  
        {  
            while(strcmp(str,"8")!=0){  
                fscanf(fp,"%s\n",str);  
            }  
            fscanf(fp,"%s\n",LayerName);//LayerName  
              
            while(strcmp(str,"70")!=0){//形态标志  
                fscanf(fp,"%s\n",str);  
            }  
            fscanf(fp,"%s\n",str2);  
            //  
            if(strcmp(str2,"64")==0)//  
            {  
                  
            }  
            //  
            if(strcmp(str2,"8")==0 || strcmp(str2,"9")==0)  
            {  
            }  
            //  
            if(strcmp(str2,"17")==0 || strcmp(str2,"49")==0 || strcmp(str2,"16")==0)  
            {  
                  
            }  
        }  
        ////////////////////////////////////////////////  
  }  
  
}  
int main(int argc, char **argv)
{

    if(argc>1)
    {
       FILE *fp=NULL;//声明文件指针  
  
            //打开文件，“rb” 只读打开一个二进制文件，只允许读数据,返回文件指针给fp  
            if((fp=fopen(argv[1],"rb"))==NULL)//如果文件打开出错  
            {  
                //打印二进制文件打开时出错的错误码  
                fprintf(stderr, "%s \n", strerror(errno));  
            }  
            else//如果文件打开正确  
            {  
                ReadDxfFile(fp);//读取DXF文件，并将数据存入CImplicitModelView类的二维vector：DXF3Dface中  
            }  
    }
  
    return 0;
}


