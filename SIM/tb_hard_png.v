
//--------------------------------------------------------------------------------------------------------
// Module  : tb_hard_png
// Type    : simulation, top
// Standard: Verilog 2001 (IEEE1364-2001)
// Function: testbench for hard_png
//--------------------------------------------------------------------------------------------------------

`timescale 1ps/1ps // 时间尺度预编译指令 时间单位/时间精度 // 时间单位：定义仿真过程所有与时间相关量的单位; 时间精度：决定时间相关量的精度及仿真显示的最小刻度


`define START_NO  1       // first png file number to decode
`define FINAL_NO  7 // 176 // 14      // last png file number to decode

`define IN_PNG_FILE_FOMRAT    "data/CityScapes/renamed/%03d.png" // "data/PngSuite-2017jul19/renamed/%03d.png" // "data/test_image/img%02d.png"
`define OUT_TXT_FILE_FORMAT   "output/CityScapes/sample_suite/txt/%03d.txt" // "output/PngSuite-2017jul19/txt/%03d.txt" // "output/test_image/txt/out%02d.txt" // 需要提前 mkdir


module tb_hard_png ();

initial $dumpvars(1, tb_hard_png); // dump all signals to waveform file


reg rstn = 1'b0;
reg clk  = 1'b1;
always #10000 clk = ~clk;    // 50MHz ? 仿真中使用“#数字”表示延时相应时间单位的时间，每 10000 ps 翻转一次，周期 20000 的时钟，即 50MHz
initial begin repeat(4) @(posedge clk); rstn<=1'b1; end // 4 个时钟周期后开始工作



reg          istart = 1'b0;
reg          ivalid = 1'b0;
wire         iready;
reg  [ 7:0]  ibyte  = 0;

wire         ostart;
wire [ 2:0]  colortype;
wire [13:0]  width;
wire [31:0]  height;

wire         ovalid;
wire [ 7:0]  opixelr, opixelg, opixelb, opixela;



hard_png hard_png_i (
    .rstn      ( rstn      ),
    .clk       ( clk       ),
    // data input
    .istart    ( istart    ),
    .ivalid    ( ivalid    ),
    .iready    ( iready    ),
    .ibyte     ( ibyte     ),
    // image size output
    .ostart    ( ostart    ),
    .colortype ( colortype ),
    .width     ( width     ),
    .height    ( height    ),
    // data output
    .ovalid    ( ovalid    ),
    .opixelr   ( opixelr   ),
    .opixelg   ( opixelg   ),
    .opixelb   ( opixelb   ),
    .opixela   ( opixela   )
);



integer fptxt = 0, fppng = 0; // file pointers
reg [256*8:1] fname_png;
reg [256*8:1] fname_txt;
integer png_no = 0;
integer txt_no = 0;
integer ii; // loop index
integer cyccnt = 0; // cycle count
integer bytecnt = 0;

initial begin
    // 在一个initial块中启动两个并行的线程，并在所有线程完成后等待100个时钟周期。
    while(~rstn) @(posedge clk); // while循环等待复位(rstn)信号变为逻辑1。它有效地停止模拟，直到复位信号解除。
    
    fork
        // thread: input png file
        for(png_no=`START_NO; png_no<=`FINAL_NO; png_no=png_no+1) begin
            istart <= 1'b1; // Istart设置为1，表示开始处理。然后在时钟(时钟)的一个上升沿后清除它。
            @ (posedge clk);
            istart <= 1'b0;
            
            $sformat(fname_png, `IN_PNG_FILE_FOMRAT , png_no);
            $sformat(fname_txt, `OUT_TXT_FILE_FORMAT , png_no); // 输入时，同步生成输出文件名
            
            fppng = $fopen(fname_png, "rb"); // 读 png 文件
            if(fppng == 0) begin
                $error("input file %s open failed", fname_png);
                $finish; // 提前结束仿真
            end
            cyccnt = 0;
            bytecnt = 0;
            
            $display("\nstart to decode %30s", fname_png ); // 打印信息，自动换行
            
            ibyte <= $fgetc(fppng); // 读取一个字节
            while( !$feof(fppng) ) @(posedge clk) begin // 在时钟的每个上升沿(clk)处执行
                if(~ivalid | iready ) begin
                    ivalid <= 1'b1;                   // A. use this to always try to input a byte to hard_png (no bubble, will get maximum throughput)
                    //ivalid <= ($random % 3) == 0;     // B. use this to add random bubbles to the input stream of hard_png. (Although the maximum throughput cannot be achieved, it allows input with mismatched rate, which is more common in the actual engineering scenarios)
                end
                if( ivalid & iready ) begin
                    ibyte <= $fgetc(fppng);
                    bytecnt = bytecnt + 1;
                end
                cyccnt = cyccnt + 1;
            end
            ivalid <= 1'b0;
            
            $fclose(fppng);
            $display("image %30s decode done, input %d bytes in %d cycles, throughput=%f byte/cycle", fname_png, bytecnt, cyccnt, (1.0*bytecnt)/cyccnt );
        end
        
        
        // thread: output txt file
        for(txt_no=`START_NO; txt_no<=`FINAL_NO; txt_no=txt_no+1) begin
            // $sformat(fname_txt, `OUT_TXT_FILE_FORMAT , txt_no);
        
            while(~ostart) @ (posedge clk); // 等待输出开始，但是有图片解码失败，会一直等待下个处理成功的图片，并且文件名 i 会被 j 覆盖(i > j)
            $display("decode result:  colortype:%1d  width:%1d  height:%1d", colortype, width, height);
            
            fptxt = $fopen(fname_txt, "w");
            if(fptxt != 0)
                $fwrite(fptxt, "decode result:  colortype:%1d  width:%1d  height:%1d\n", colortype, width, height);
            else begin
                $error("output txt file %30s open failed", fname_txt);
                $finish;
            end
            
            for(ii=0; ii<width*height; ii=ii+1) begin
                @ (posedge clk);
                while(~ovalid) @ (posedge clk);
                $fwrite(fptxt, "%02x%02x%02x%02x ", opixelr, opixelg, opixelb, opixela);
                if( (ii % (width*height/10)) == 0 ) $display("%d/%d", ii, width*height);
            end
            
            $fclose(fptxt);
        end
    join
    
    repeat(100) @ (posedge clk);
    $finish; // 结束仿真
end


endmodule
