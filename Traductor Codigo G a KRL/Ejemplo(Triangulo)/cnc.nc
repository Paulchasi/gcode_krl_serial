

G00 X0 Y0 Z30 
G00 X0 Y0 Z5       ; Movimiento rápido al punto inicial con Z en posición segura
G00 Z0             ; Descenso rápido al plano de trabajo

G01 Z-1            ; Profundidad de corte de 2 mm
G01 X50 Y0         ; Trazo del primer lado (50 mm)
G01 X25 Y43.3      ; Trazo del segundo lado
G01 X0 Y0          ; Trazo del tercer lado
Z5
G01 Z-2            ; Profundidad de corte de 2 mm
G01 X50 Y0         ; Trazo del primer lado (50 mm)
G01 X25 Y43.3      ; Trazo del segundo lado
G01 X0 Y0          ; Trazo del tercer lado
Z5
G01 Z-3            ; Profundidad de corte de 2 mm
G01 X50 Y0         ; Trazo del primer lado (50 mm)
G01 X25 Y43.3      ; Trazo del segundo lado
G01 X0 Y0          ; Trazo del tercer lado
Z5
G01 Z-4            ; Profundidad de corte de 2 mm
G01 X50 Y0         ; Trazo del primer lado (50 mm)
G01 X25 Y43.3      ; Trazo del segundo lado
G01 X0 Y0          ; Trazo del tercer lado
Z5
G01 Z-5            ; Profundidad de corte de 2 mm
G01 X50 Y0         ; Trazo del primer lado (50 mm)
G01 X25 Y43.3      ; Trazo del segundo lado
G01 X0 Y0          ; Trazo del tercer lado


G00 Z5             ; Elevación a posición segura
G00 X0 Y0 Z30 
