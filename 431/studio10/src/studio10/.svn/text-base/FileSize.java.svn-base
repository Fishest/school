package studio10;
//
// Included for your reference -- this file is not used in this studio
//
import java.io.*;
public class FileSize implements Runnable {
   private String file;
   private long size;
   public FileSize(String file) {
      this.file = file;
      this.size = 0L;
   }
   public long getSize() { return size; }
   public String toString() {
      return "Size of " + file + " = " + getSize();
   }
   public void run() {
      try {
         File f = new File(file);
         FileInputStream fis = new FileInputStream(f);
         int b = 0;
         b = fis.read();
         while (b != -1) {
            ++size;
            b = fis.read();
         }
      } catch(Throwable t) {
         throw new Error(""+t);
      } 
   }
   public static void main(String[] args) {
      if (args.length != 1)
         throw new Error("Usage:  java FileSize filename");
      FileSize fs = new FileSize(args[0]);
      fs.run();
      System.out.println("" + fs);
   }
}
