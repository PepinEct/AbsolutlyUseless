import java.util.Scanner;
import java.io.FileWriter;

class ThreadRunner{
    static class filler extends Thread{
        int picker;
        int times;
        String dir;
        String template;
        int base=0;
        
    
        public void setArgs(int picker, int times, String dir, String template){
            this.picker = picker;
            this.times = times;
            this.dir = dir;
            this.template = template;
        }
    
    
        public void run(){
            //stuff in the thread
            for(int x = 0; x != picker-1; x++){
                this.base += times;
            }
            //System.out.println("Thread "+picker+" base: "+base);
            System.out.println("Started thread: "+picker);
            for(int x = 0; x!=times; x++){
            try {
                FileWriter file = new FileWriter(dir+"out"+(base+x)+".txt");
                file.write(template);
                file.close();
            } catch (Exception e) {
                // TODO: handle exception
                //e.printStackTrace();
            }
        }
            System.out.println("Stopped thread: "+picker);
        }
        
    }
    
    static int threads = 3;
    static int picker = 1;
    static int times = 100;
    static String dir = "temp/";
    static String template = "";
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter amount Threads:");
        threads = Integer.parseInt(sc.nextLine());
        System.out.println("Enter amount Times:");
        times = Integer.parseInt(sc.nextLine());
        sc.close();


        System.out.println("Generating template");
        for(int x = 0; x != 100000; x++){
            template+="xxxxXxxxx";
        }
        
        for(int x = 0; x!=threads; x++){
            filler y = new filler();
            Thread t1 = new Thread(y);
            
            y.setArgs(picker, times, dir, template);
            picker++;
            t1.start();
        }
        }
}