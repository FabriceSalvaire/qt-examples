```
QSGNode : The base class for all nodes in the scene graph
    QSGBasicGeometryNode : Serves as a baseclass for geometry based nodes
        QSGGeometryNode : Used for all rendered content in the scene graph
            QSGImageNode : Provided for convenience to easily draw textured content using the QML scene graph
            QSGRectangleNode : Convenience class for drawing solid filled rectangles using scenegraph
            QSGSimpleRectNode : Convenience class for drawing solid filled rectangles using scenegraph
            QSGSimpleTextureNode : Provided for convenience to easily draw textured content using the QML scene graph
        QSGClipNode : Implements the clipping functionality in the scene graph
    QSGOpacityNode : Used to change opacity of nodes
    QSGRenderNode : Represents a set of custom rendering commands targeting the graphics API that is in use by the scenegraph
                    A convenience scene graph node to wrap raw OpenGL rendering.
    QSGTransformNode : Implements transformations in the scene graph

QSGGeometry : Low-level storage for graphics primitives in the Qt Quick Scene Graph
QSGGeometry::Attribute : QSGGeometry::Attribute describes a single vertex attribute in a QSGGeometry
QSGGeometry::AttributeSet : QSGGeometry::AttributeSet describes how the vertices in a QSGGeometry are built up
QSGGeometry::ColoredPoint2D : QSGGeometry::ColoredPoint2D struct is a convenience struct for accessing 2D Points with a color
QSGGeometry::Point2D : QSGGeometry::Point2D struct is a convenience struct for accessing 2D Points
QSGGeometry::TexturedPoint2D : QSGGeometry::TexturedPoint2D struct is a convenience struct for accessing 2D Points with texture coordinates

QSGMaterialShader : Represents a graphics API independent shader program
QSGMaterialShader::GraphicsPipelineState : Describes state changes that the material wants to apply to the currently active graphics pipeline state
QSGMaterialShader::RenderState : Encapsulates the current rendering state during a call to QSGMaterialShader::updateUniformData() and the other update type of functions

QSGMaterial : Encapsulates rendering state for a shader program
    QSGFlatColorMaterial : Convenient way of rendering solid colored geometry in the scene graph
    QSGOpaqueTextureMaterial : Convenient way of rendering textured geometry in the scene graph
        QSGTextureMaterial : Convenient way of rendering textured geometry in the scene graph
    QSGVertexColorMaterial : Convenient way of rendering per-vertex colored geometry in the scene graph

QSGMaterialType : Used as a unique type token in combination with QSGMaterial

QSGTexture : The base class for textures used in the scene graph
    QSGDynamicTexture : Serves as a baseclass for dynamically changing textures, such as content that is rendered to FBO's

QSGTextureProvider : Encapsulates texture based entities in QML
                     For example, to render textures from QML items
                     See examples/quick/scenegraph/twotextureproviders https://doc.qt.io/qt-6/qtquick-scenegraph-twotextureproviders-example.html

QSGRendererInterface : An interface providing access to some of the graphics API specific internals of the scenegraph
                       Renderer interfaces allow accessing graphics API specific functionality in the scenegraph. Such
                       internals are not typically exposed. However, when integrating custom rendering via QSGRenderNode
                       for example, it may become necessary to query certain values, for instance the graphics device
                       (e.g. the Direct3D or Vulkan device) that is used by the scenegraph.
```
