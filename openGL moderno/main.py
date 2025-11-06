import glfw
from OpenGL.GL import *
import numpy as np
import math

def matrix_escala(sx,sy,sz):
    return np.array([
        [sx,0,0,0],
        [0,sy,0,0],
        [0,0,sz,0],
        [0,0,0,1]
    ],dtype=np.float32)
    
def rotate_z(angulo_radianos):
    c = math.cos(angulo_radianos)
    s = math.sin(angulo_radianos)
    return np.array([
        [ c, -s, 0, 0],
        [ s,  c, 0, 0],
        [ 0,  0, 1, 0],
        [ 0,  0, 0, 1]
    ], dtype=np.float32)
    
def matrix_translacao(tx,ty,tz):
    return np.array([
        [1,0,0,tx],
        [0,1,0,ty],
        [0,0,1,tz],
        [0,0,0,1]
    ],dtype=np.float32)


def main():
    # 1. Initialize GLFW
    if not glfw.init():
        print("Erro: Não foi possível inicializar o GLFW.")
        return

    # Request OpenGL Core Profile 3.3
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    # glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)  # Uncomment if needed (MacOS)

    # 2. Criação da Janela de Aplicação
    window = glfw.create_window(800, 600, "Esqueleto OpenGL Core (2D)", None, None)
    if not window:
        glfw.terminate()
        print("Erro: Não foi possível criar a janela GLFW.")
        return

    # Torna o contexto da janela o contexto atual do thread
    glfw.make_context_current(window)
    
    # 3. Criação dos VAO/VBO e Shaders (Vertex + Frag)
    # 3.1 VAO/VBO
    # 3.2 Shaders
    # 3.3 Programa (shaders)
    
    vertices = np.array([
# Posição (x, y, z) Cor (r, g, b)
        0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
        -0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
        0.0, 0.5, 0.0, 0.0, 0.0, 1.0
        ], dtype=np.float32)
    
    vertices_quadrado = np.array([
    # Triângulo 1 (parte esquerda do quadrado)
    -0.2, -0.2, 0.0, 1.0, 1.0, 0.0,
     0.2, -0.2, 0.0, 0.0, 1.0, 1.0,
    -0.2,  0.2, 0.0, 1.0, 0.0, 1.0,

    # Triângulo 2 (parte direita do quadrado)
     0.2, -0.2, 0.0, 0.0, 1.0, 1.0,
     0.2,  0.2, 0.0, 1.0, 0.5, 0.0,
    -0.2,  0.2, 0.0, 1.0, 0.0, 1.0,
], dtype=np.float32)

    
    vbo = glGenBuffers(1) #cria a variavel vbo, é criado um buffer, espaço na memória (onde armazenamos um local na gpu para realizar a leitura dos verticese)
    glBindBuffer(GL_ARRAY_BUFFER, vbo) #vincula o buffer com o vbo
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW) # aqui precisa apresentar o que são os dados que enviaremos, no caso este é um gl.array, o vertices
    # que passaremos são um array
    
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    
    # Atributo 0 → posição (x, y, z)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(
        0,                    # índice do atributo no shader
        3,                    # quantidade de valores (x,y,z)
        GL_FLOAT,             # tipo
        GL_FALSE,             # normalizado?
        6 * 4,                # stride (tamanho total de 1 vértice)
        ctypes.c_void_p(0)    # offset inicial = começa em 0
    )
    
    # Atributo 1 → cor (r, g, b)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(
        1,                    # índice do atributo no shader
        3,                    # quantidade de valores (r,g,b)
        GL_FLOAT,
        GL_FALSE,
        6 * 4,                # stride igual porque está tudo intercalado
        ctypes.c_void_p(3 * 4) # offset: pula os 3 floats de posicao, os 3 (x,y,z) possuem 12 bt, por isso 3*4, pulamos os 12 primeiros bt e chegamos diretamente na cor
    )
    # temos 6 valores (x,y,z,r,g,b) todos estes sao floats32 que ocupam 4bt, por isso no stride o valor é de 6*4
    
    # --- logica do quadrados --- 
    
    vbo_quadrados = glGenBuffers(1) #cria a variavel vbo, é criado um buffer, espaço na memória (onde armazenamos um local na gpu para realizar a leitura dos verticese)
    glBindBuffer(GL_ARRAY_BUFFER, vbo_quadrados) #vincula o buffer com o vbo
    glBufferData(GL_ARRAY_BUFFER, vertices_quadrado.nbytes, vertices_quadrado, GL_STATIC_DRAW) # aqui precisa apresentar o que são os dados que enviaremos, no caso este é um gl.array, o vertices
    # que passaremos são um array
    
    vao_quadrados = glGenVertexArrays(1)
    glBindVertexArray(vao_quadrados)
    
    # Atributo 0 → posição (x, y, z)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(
        0,                    # índice do atributo no shader
        3,                    # quantidade de valores (x,y,z)
        GL_FLOAT,             # tipo
        GL_FALSE,             # normalizado?
        6 * 4,                # stride (tamanho total de 1 vértice)
        ctypes.c_void_p(0)    # offset inicial = começa em 0
    )
    
    # Atributo 1 → cor (r, g, b)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(
        1,                    # índice do atributo no shader
        3,                    # quantidade de valores (r,g,b)
        GL_FLOAT,
        GL_FALSE,
        6 * 4,                # stride igual porque está tudo intercalado
        ctypes.c_void_p(3 * 4) # offset: pula os 3 floats de posicao, os 3 (x,y,z) possuem 12 bt, por isso 3*4, pulamos os 12 primeiros bt e chegamos diretamente na cor
    )
    # temos 6 valores (x,y,z,r,g,b) todos estes sao floats32 que ocupam 4bt, por isso no stride o valor é de 6*4
    
    
    
    
    # criacao do vertex shader
    shader_vertex = glCreateShader(GL_VERTEX_SHADER) # cria um shader do tipo vertex
    with open('vertex_shader.glsl', 'r') as file:  # abre o arquivo onde esta o vertex shader
        glShaderSource(shader_vertex, file.read()) # faz a união do shader criado com o arquivo lido
    glCompileShader(shader_vertex) #compila o shader
    glGetShaderiv(shader_vertex, GL_COMPILE_STATUS) #verifica o status e ve se o shader nao deu erro
    print(glGetShaderInfoLog(shader_vertex))
    
    # criacao do fragment shader
    shader_fragment = glCreateShader(GL_FRAGMENT_SHADER)
    with open('fragment_shader.glsl','r') as file:
        glShaderSource(shader_fragment,file.read())
    glCompileShader(shader_fragment)
    glGetShaderiv(shader_fragment, GL_COMPILE_STATUS) #verifica o status e ve se o shader nao deu erro
    print(glGetShaderInfoLog(shader_fragment))
    
    
    # --- agora temos que criar o program que usará os shaders criados
    shader_program = glCreateProgram()
    glAttachShader(shader_program, shader_vertex)
    glAttachShader(shader_program, shader_fragment)
    glLinkProgram(shader_program)
    
    
     # programa do fragment quadrado vermelho
    shader_fragment_vermelho = glCreateShader(GL_FRAGMENT_SHADER)
    with open('fragment_shader_quadrado.glsl','r') as file:
        glShaderSource(shader_fragment_vermelho,file.read())
    glCompileShader(shader_fragment_vermelho)
    glGetShaderiv(shader_fragment_vermelho, GL_COMPILE_STATUS) #verifica o status e ve se o shader nao deu erro
    print(glGetShaderInfoLog(shader_fragment_vermelho))
    
    #criando o programa apenas para o quadrado
    
    shader_program_quadrado = glCreateProgram()
    
    
    glAttachShader(shader_program_quadrado , shader_vertex)
    
    glAttachShader(shader_program_quadrado , shader_fragment_vermelho)
    
    glLinkProgram(shader_program_quadrado)
    
    glGetProgramiv(shader_program_quadrado, GL_LINK_STATUS)
    print(glGetProgramInfoLog(shader_program_quadrado))

    

    

    #Espeficamos as operações de viewport
    glViewport(0, 0, 800, 600)

    # Define a cor de fundo da janela
    glClearColor(0.3, 0.3, 0.3, 1.0)
    
    proj = np.identity(4, dtype=np.float32) 
    
    # --- efeitos de transalacao e rotacao ---
    
    # chamado das funcoes com am matrizes das operações lá do inicio do codigo
    # a multiplicação em numpy é feita com (@)
    tempo = glfw.get_time()  # pegamos o tempo em segundos pois buscamos um efeito de rotacao continua
    translation = matrix_translacao(0.3,0.0,0.0) 
    
    scale = matrix_escala(0.7,0.7,1.0) # quando matriz de escala menor do que e1.0 vai diminuindo de tamanho
    
    #model = translation @ rotation @ scale
    
    proj_loc = glGetUniformLocation(shader_program_quadrado, "uModel")
    
    

    # 4. Loop de Renderização Principal
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        # matrix de projecao, esta é a mais comum projetando em 2D
        
         # --- efeitos de transalacao e rotacao ---
    
    # chamado das funcoes com am matrizes das operações lá do inicio do codigo
    # a multiplicação em numpy é feita com (@)
        tempo = glfw.get_time()  # pegamos o tempo em segundos pois buscamos um efeito de rotacao continua
        translation = matrix_translacao(0.3,0.0,0.0) 
        rotation = rotate_z(tempo)
        scale = matrix_escala(0.7,0.7,1.0) # quando matriz de escala menor do que e1.0 vai diminuindo de tamanho
        model = translation @ rotation @ scale

        # Vincular o programa (shaders) que fará as operações
        # Envia a matriz de projeção para o shader
        
        

        # >>> Espaço para o seu código de desenho aqui (Core) <<<
        # Vincular VAOs/VBOs dos seus desenhos
        # Chamadas de desenho das primitivas (usando programa/shader vinculado)
        
        #O VBO não precisa ser reconfigurado ou reenviado a cada frame; ele já está
        #na GPU, só é necessário ativar o VAO que diz como e onde ler
        glUseProgram(shader_program)
        glBindVertexArray(vao)
        uModel_loc_tri = glGetUniformLocation(shader_program, "uModel")
        glUniformMatrix4fv(uModel_loc_tri, 1, GL_FALSE, proj.flatten())
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glBindVertexArray(0) 
        
        # ---- vamos criar uma matrix de rotacao para o nosso quadrado ---- 
        
   
        
        # --- desenhando o quadrados ---
        glUseProgram(shader_program_quadrado)
        glBindVertexArray(vao_quadrados)
        
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, (proj @ model).flatten())
        
        
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindVertexArray(0)
        
        # Desvincular VAOs/VBOs
        # Desvincular o programa (shaders)


        # Verifica e processa eventos da janela
        glfw.poll_events()

        # Troca os buffers front e back para exibir a imagem renderizada
        glfw.swap_buffers(window)


    # 5. Finalização
    glfw.terminate()
    #Também será necessário limpar os VAOs/VBOs e Program/Shaders
    
    glDeleteVertexArrays(1, [vao])
    glDeleteBuffers(1, [vbo])

if __name__ == "__main__":
    main()
