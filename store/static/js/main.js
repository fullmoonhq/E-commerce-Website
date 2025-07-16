$(document).ready (function()
{
    $('.increment-btn').click(function(e) 
    {
        e.preventDefault();

        let increment = $(this).closest('.pdata').find('.qty').val();
        let value = parseInt(increment,10)
        value - isNaN(value) ? 0 : value;

        if (value < 20)
        {
            value++;
            $(this).closest('.pdata').find('.qty').val(value);
        }
    });

    $('.decrement-btn').click(function(e) 
    {
        e.preventDefault;

        let increment = $(this).closest('.pdata').find('.qty').val();
        let value = parseInt(increment,10)
        value = isNaN(value) ? 0 : value;

        if (value > 1)
        {
            value--;
            $(this).closest('.pdata').find('.qty').val(value);
        }
    });

    $('.cart').click(function(e) 
        {
            e.preventDefault();

            let pid = $(this).closest('.pdata').find('.pid').val();
            let pqty = $(this).closest('.pdata').find('.qty').val(); 
            let csrftoken = $('input[name=csrfmiddlewaretoken]').val();

            $.ajax({
            method:'POST',
            url:'/addtocart',
            data:{'pid': pid,'pqty': pqty,'csrfmiddlewaretoken': csrftoken}
            })
            .done(function(response){
            console.log(response)
            })
            .fail(function(response){
            console.log(response)
            });

            $.ajax();         
    });

    $('.changeqty').click(function(e) 
        {
            e.preventDefault();

            let pid = $(this).closest('.pdata').find('.pid').val();
            let pqty = $(this).closest('.pdata').find('.qty').val(); 
            let csrftoken = $('input[name=csrfmiddlewaretoken]').val();

            $.ajax({
            method:'POST',
            url:'/updatecartitem',
            data:{'pid': pid,'pqty': pqty,'csrfmiddlewaretoken': csrftoken}
            })
            .done(function(response){
            console.log(response)
            })
            .fail(function(response){
            console.log(response)
            });

            $.ajax();         
    });

    $('.delete-cartitem').click(function(e) 
        {
            e.preventDefault();

            let pid = $(this).closest('.pdata').find('.pid').val();
            let csrftoken = $('input[name=csrfmiddlewaretoken]').val();

            $.ajax({
                method:'POST',
                url:'/removecartitem',
                data:{'pid': pid,'csrfmiddlewaretoken': csrftoken},
                success:(function(response){
                    $('.cartitems').load(location.href + '.cartitems');
                })
            })
            .done(function(response){
                console.log(response)
            })
            .fail(function(response){
                console.log(response)
            });

            $.ajax();         
    });



    $('.wishlist').click(function(e) 
        {
            e.preventDefault();

            let pid = $(this).closest('.pdata').find('.pid').val();
            let csrftoken = $('input[name=csrfmiddlewaretoken]').val();

            $.ajax({
                method:'POST',
                url:'/addtowishlist',
                data:{'pid': pid,'csrfmiddlewaretoken': csrftoken}
            })
            .done(function(response){
                console.log(response)
            })
            .fail(function(response){
                console.log(response)
            });

            $.ajax();         
    });

    $(document).on('click','.remove-wishlist-item',function(e) 
   
        {
            e.preventDefault();

            let pid = $(this).closest('.pdata').find('.pid').val();
            let csrftoken = $('input[name=csrfmiddlewaretoken]').val();

            $.ajax({
                method:'POST',
                url:'/removewishlistitem',
                data:{'pid': pid,'csrfmiddlewaretoken': csrftoken},
                success:(function(response){
                    $('.wishlistitems').load(location.href + '.wishlistitems');
                })
            })
            .done(function(response){
                console.log(response)
            })
            .fail(function(response){
                console.log(response)
            });

            $.ajax();         
    });

});