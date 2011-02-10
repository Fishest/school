package org.school.core.loader

object FileLoader extends AbstractLoader {

    override def supports(location:String) =
        location.startsWith("file://")
}
