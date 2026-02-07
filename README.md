usage: avtools [-h] [-d DOWNLOAD] [-F FILE] [-al] [-o OUTPUT] [-v] [--cut CUT] [--effect] [--join JOIN]
               [--midnight MIDNIGHT]

Canivete Suíço da edição vídeos em geral por linha de comandos.

options:
  -h, --help            show this help message and exit
  -d DOWNLOAD, --download DOWNLOAD
                        URL do vídeo a ser processado.
  -F FILE, --file FILE  Caminho do arquivo de vídeo a ser editado.
  -al, --auto-legend    Gera legendas automáticas para o vídeo.
  -o OUTPUT, --output OUTPUT
                        Caminho do arquivo de saída.
  -v, --version         show program's version number and exit
  --cut CUT             Corta o vídeo de acordo com os parâmetros informados. Exemplo: --cut "start=00:01:00
                        end=00:02:00"
  --effect              Ativa o modo de edição interativa do vídeo. (Em desenvolvimento)
  --join JOIN           Concatena múltiplos vídeos. Exemplo: --join "video1.mp4 video2.mp4 video3.mp4" (Em
                        desenvolvimento)
  --midnight MIDNIGHT   Aplica o efeito 'midnight' em um vídeo. Exemplo: --midnight "video_superior.mp4
                        video_inferior.mp4" (Em desenvolvimento)

