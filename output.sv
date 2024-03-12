module fsm(input wire clk, input wire rst, input wire x, input wire y, output reg [1:0] out);
reg [2:0] s, ns;
reg [1:0] nout;

always@(*) begin
ns=3'b100;
nout=out;
case(s)
3'b100: begin
ns=3'b100;
if(x) begin
ns=3'b010;
nout=2'b10;
end
if(y) begin
ns=3'b001;
nout=2'b01;
end
end
3'b010: begin
ns=3'b010;
if(x) begin
ns=3'b001;
nout=2'b01;
end
if(y) begin
ns=3'b100;
nout=2'b10;
end
end
3'b001: begin
ns=3'b001;
if(x) begin
ns=3'b010;
nout=2'b01;
end
if(y) begin
ns=3'b100;
nout=2'b01;
end
end
endcase
end

always@(posedge clk) begin
if(rst) begin
s<=3'b100;
out<=2'b00;
end
else begin
s<=ns;
out<=nout;
end
end

endmodule