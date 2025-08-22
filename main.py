#!/usr/bin/env python3
"""
Punto de entrada principal para el servidor MCP de YouTrack
"""
import argparse
from src.server import run_server


def main():
    parser = argparse.ArgumentParser(description="Servidor MCP para YouTrack")
    parser.add_argument(
        "--timeout", 
        type=int, 
        default=30,
        help="Timeout para requests HTTP en segundos (default: 30)"
    )
    parser.add_argument(
        "--finished-states",
        type=str,
        default="Fixed,Verified",
        help="Estados considerados como terminados, separados por comas (default: 'Fixed,Verified')"
    )
    
    args = parser.parse_args()
    
    # Ejecutar servidor con configuración
    run_server(timeout=args.timeout, finished_states=args.finished_states)


if __name__ == "__main__":
    main()
