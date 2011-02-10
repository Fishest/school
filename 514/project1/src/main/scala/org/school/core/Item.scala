package org.school.core

import java.io.Serializable

/**
 * Represents a single item from the dataset
 *
 * @param value The value of this item
 * @param confidence The confidence of this item
 * @param support The support of this item
 */
class Item(var value:String, val frequencey:Int, val confidence:Double, val support:Double)
    extends Serializable {

    def this(value:String) = this(value, 1, 1, 1)
}
