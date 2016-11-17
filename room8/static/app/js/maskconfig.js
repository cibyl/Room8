$(document).ready(function(){
  $('.cep').mask('00000-000');
  $('.cpf').mask('000.000.000-00#');
  $('.cnpj').mask('00.000.000/0000-00');
  $('.celular').mask('(00) 0000-00000');
  $('.valor-monetario').mask('000000000,00', {reverse:true});
});
