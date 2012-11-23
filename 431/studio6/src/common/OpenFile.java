package common;

import java.net.*;
import java.io.*;

public class OpenFile extends DataInputStream {

   static private BufferedInputStream dothework(String f) {
         URL u;
         DataInputStream datainput;
         InputStream input;
         if (f.trim().equals("")) {
        	    return new BufferedInputStream(System.in);
         }
         else if (f.startsWith("http:")) {
            try {
               u = new URL(f);
            } catch (MalformedURLException ex) 
                 { throw new Error(ex.toString()); }
            try {
               input = u.openStream();
               System.out.println("URL stream open");
            }
            catch (IOException ex) { throw new Error(ex.toString()); }
         }
         else {
            try {
               input = new FileInputStream(f);
            } catch (Exception e) {throw new Error(e.toString()); }
         }
         return (new BufferedInputStream(input));
   }
   public OpenFile(String f) {
         super(dothework(f));
   }
}
