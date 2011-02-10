package org.school.core.loader

object LoaderFactory {

    private val loaders = List[AbstractLoader](
        FileLoader, HttpLoader,
    )

    def load(location:String) : Option[AbstractLoader] = {
        for (loader <- loaders) {
            if (loader.supports(location))
                return Some(loader)
        }
        return None
    }
}
