package org.school.core.loader

/**
 */
object HttpLoader extends AbstractLoader {

    /**
     * Tests if this loader supports loading the file
     * at the referenced location.
     *
     * @param location The URI that should be tested
     * @return true if this loader supports this location
     */
    override def supports(location:String) =
        location.startsWith("http://")  ||
        location.startsWith("https://") ||
        location.startsWith("ftp://")   ||
        location.startsWith("ftps://")

    /**
     * Loads the specified location
     *
     * @param location The URI that should be loaded
     * @return An iterator around the given source
     */
    override def load(location:String) =
        io.Source.fromFile(location).getURL
}
