package org.school.core

import java.io.Serializable

/**
 * Represents a set of items from the dataset
 *
 * @param items The items composing this Item set
 */
class ItemSet private (val items:List[Item])
    extends Serializable {
}

object ItemSet {
    def apply(items:List[Item]) = new ItemSet(items)
    def apply(items:Item*) = new ItemSet(items.toList)
}
