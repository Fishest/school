package org.school.association

import org.school.core.{Item, ItemSet}

class Apriori(val database:List[Item]) {

    def process() : List[AssociationRule] {

        val frequent = generateFrequents1(database)
        do
    }

    private def generateCandidate(rules:List[AssociationRule])
        : List[AssociationRule] {
    }

    private def generateFrequents1(items:List[Item])
        : List[AssociationRule] {
        items.filter { _.support > support }
    }

    private def generateFrequentsN(items:List[ItemSet], count:Int)
        : List[ItemSet] {
    }
}

// vim: set ts=4 sw=4 et:
