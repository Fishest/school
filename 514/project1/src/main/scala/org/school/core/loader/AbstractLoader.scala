package org.school.core.loader

/**
 */
trait AbstractLoader {

    /**
     * Tests if this loader supports loading the file
     * at the referenced location.
     *
     * @param location The URI that should be tested
     * @return true if this loader supports this location
     */
    def supports(location:String) : Boolean

    /**
     * Loads the specified location
     *
     * @param location The URI that should be loaded
     * @return An iterator around the given source
     */
    def load(location:String) : Iterator[String]
}
