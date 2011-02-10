package org.school.core.loader

object HttpLoader extends AbstractLoader {

    override def supports(location:String) =
        location.startsWith("http://")  ||
        location.startsWith("https://") ||
        location.startsWith("ftp://")   ||
        location.startsWith("ftps://")
}
