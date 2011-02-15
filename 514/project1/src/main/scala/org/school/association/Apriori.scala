package org.school.association

import org.school.core.{Item, ItemSet}

class Apriori(val database:List[Item], var minsup:Double, var minconf:Double) {

    def process() : List[AssociationRule] {

        var frequents  = List[ItemSet]()
        var candidates = generateCanidates(database)
        while (candidates.nonEmpty) {

            for 
            frequents = frequents :+ candidates
        }
        frequents
    }

    private def generateCandidates(items:List[Item])
        : List[ItemSet] {
        items.filter { _.support >= minsup }.map { ItemSet(_) }
    }

    private def generateCandidates(items:List[ItemSet], count:Int)
        : List[ItemSet] {
    }

    private def generateSubsets(items:List[ItemSet])
        : List[ItemSet] {
    }
}

// vim: set ts=4 sw=4 et:
