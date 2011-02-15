package org.school.core.format

import org.school.core.ItemSet

/**
 */
trait AbstractFormat {

    /**
     * Processes the given source into ItemSets
     *
     * @param source The source to be processed
     * @return The processed list iterator
     */
    def process(source:Iterator[String]) : List[ItemSet]
}
