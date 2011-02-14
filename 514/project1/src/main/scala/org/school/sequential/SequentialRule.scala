package org.school.sequential

import java.io.Serializable
import org.school.core.Item

/**
 * Represents an sequential rule derived from the dataset
 */
class SequentialRule(var premise:List[Item], var consequence : List[Item])
    extends Serializable {

    var confidence : Double = _
    var support : Double = _

    def this() = this(null, null)
}


