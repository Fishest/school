package org.school.association

import java.io.Serializable
import org.school.core.Item

/**
 * Represents an association rule derived from the dataset
 */
class AssociationRule(var premise:List[Item], var consequence : List[Item])
    extends Serializable {

    def this() = this(null, null)
}


