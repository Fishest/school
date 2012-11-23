/*
 * CSE 431S Programming Assignment 2
 */

package cse431s.lab2;

import java.io.BufferedInputStream;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.net.URL;

/**
 * Opens either a file or a URL as a buffered DataInputStream.
 */
public class Opener {

    /**
     * Opens a file or a URL as a data input stream.
     * 
     * @param name
     *            the file name or URL.
     * @return an input stream tied to the file or URL.
     */
    public static DataInputStream open(String name) {
        InputStream istream;
        URL url;

        if (name.startsWith("http:")) {
            try {
                url = new URL(name);
            } catch (MalformedURLException e) {
                throw new Error(e.toString());
            }

            try {
                istream = url.openStream();
            } catch (IOException e) {
                throw new Error(e.toString());
            }
        } else {
            try {
                istream = new FileInputStream(name);
            } catch (Exception e) {
                throw new Error(e.toString());
            }
        }

        return new DataInputStream(new BufferedInputStream(istream));
    }
}
