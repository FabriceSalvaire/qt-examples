####################################################################################################

# https://doc.qt.io/qt-6/qtshadertools-qsb.html

# https://developer.android.com/guide/topics/graphics/opengl
# https://www.khronos.org/registry/OpenGL/specs/es/3.1/GLSL_ES_Specification_3.10.pdf
# OpenGL ES 3.1 - This API specification is supported by Android 5.0 (API level 21) and higher.
# The OpenGL ES 3.1 API is designed to work with GLSL ES v1.00, GLSL ES 3.00 and GLSL ES 3.10.

# To dump a shader
#   qsb -d point.vert.qsb

####################################################################################################

all: \
	noisy.vert.qsb 	\
	noisy.frag.qsb \
	line.vert.qsb \
	line.frag.qsb

clean:
	rm -f *.vert.qsb *.frag.qsb

rebuild: clean all

####################################################################################################

# GL_VERSION="460"
GL_VERSION="150,120,100es"

# qsb=/srv/qt/Qt/6.3.0/gcc_64/bin/qsb
# $qsb -b --glsl "150,120,100 es" --hlsl 50 --msl 12 -o noisy.vert.qsb noisy.vert

%.vert.qsb : %.vert
	qsb -b --glsl ${GL_VERSION} -o $@ $^
%.frag.qsb : %.frag
	qsb -b --glsl ${GL_VERSION} -o $@ $^

