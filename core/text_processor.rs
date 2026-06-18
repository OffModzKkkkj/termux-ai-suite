use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("Uso: ./text_processor <texto>");
        return;
    }

    let input = &args[1];
    let processed = input.to_uppercase(); // Exemplo de processamento rápido
    println!("Processado (Rust): {}", processed);
}
