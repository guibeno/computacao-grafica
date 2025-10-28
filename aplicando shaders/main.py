import glfw
from OpenGL.GL import *
import numpy as np
import cv2
import ctypes


def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        print("Erro de compilação no shader:", glGetShaderInfoLog(shader).decode())
        glDeleteShader(shader)
        return None
    return shader

def create_shader_program(vertex_shader_source, fragment_shader_source):
    vshader = compile_shader(vertex_shader_source, GL_VERTEX_SHADER)
    fshader = compile_shader(fragment_shader_source, GL_FRAGMENT_SHADER)
    shader_program = glCreateProgram()
    glAttachShader(shader_program, vshader)
    glAttachShader(shader_program, fshader)
    glLinkProgram(shader_program)
    if not glGetProgramiv(shader_program, GL_LINK_STATUS):
        print("Erro de linkagem:", glGetProgramInfoLog(shader_program).decode())
        return None
    glDeleteShader(vshader)
    glDeleteShader(fshader)
    return shader_program

def load_texture(path):
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    h, w, _ = image.shape

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, image)
    glGenerateMipmap(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)
    return texture, w, h


def main():
    if not glfw.init():
        print("Erro ao inicializar GLFW.")
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(800, 600, "Visualizador de Imagem OpenGL", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    vertices = np.array([
        #   x,     y,     s,    t,     r,    g,    b
        -1.0, -1.0,  0.0, 0.0,  1.0,  0.0,  0.0,  # vermelho
        1.0, -1.0,  1.0, 0.0,  0.0,  1.0,  0.0,  # verde
        1.0,  1.0,  1.0, 1.0,  0.0,  0.0,  1.0,  # azul
        -1.0,  1.0,  0.0, 1.0,  1.0,  1.0,  0.0,  # amarelo
    ], dtype=np.float32)



    indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)

    # Configuração dos buffers
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    ebo = glGenBuffers(1)

    glBindVertexArray(vao)

    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # posição (x, y)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 7 * vertices.itemsize, ctypes.c_void_p(0))

    # coordenadas de textura (s, t)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 7 * vertices.itemsize, ctypes.c_void_p(2 * vertices.itemsize))

    # cor (r, g, b)
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 7 * vertices.itemsize, ctypes.c_void_p(4 * vertices.itemsize))


    glBindVertexArray(0)

    with open("vertex_shader.glsl") as f:
        vertex_shader_src = f.read()
    with open("fragment_shader.glsl") as f:
        fragment_shader_src = f.read()

    shader = create_shader_program(vertex_shader_src, fragment_shader_src)

    texture, w, h = load_texture("C:\\Users\\1137015\\AppData\\Local\\Temp\\9a86756a-4efd-4b59-8277-1aabe974693f_marble_56-1K.zip.93f\\marble_56-1K\\marble_56_basecolor-1K.png")

    aspect_ratio = w / h
    glfw.set_window_size(window, int(600 * aspect_ratio), 600)

    glClearColor(0.2, 0.2, 0.2, 1.0)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(shader)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture)
        glUniform1i(glGetUniformLocation(shader, "texture1"), 0)

        glBindVertexArray(vao)
        # Define se quer textura (1) ou só cor (0)
        controle_loc = glGetUniformLocation(shader, "controle")
        glUniform1i(controle_loc, 1)  # 1 = mistura textura e cor | 0 = só cor

        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

        glfw.swap_buffers(window)
        glfw.poll_events()

    # Cleanup
    glDeleteVertexArrays(1, [vao])
    glDeleteBuffers(1, [vbo])
    glDeleteBuffers(1, [ebo])
    glDeleteTextures(1, [texture])
    glDeleteProgram(shader)
    glfw.terminate()

if __name__ == "__main__":
    main()
