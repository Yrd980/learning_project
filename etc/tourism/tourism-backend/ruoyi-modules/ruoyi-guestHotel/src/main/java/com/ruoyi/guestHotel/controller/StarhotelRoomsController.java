package com.ruoyi.guestHotel.controller;

import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.guestHotel.domain.*;
import com.ruoyi.guestHotel.domain.VO.StarhotelReviewsVO;
import com.ruoyi.guestHotel.service.IStarhotelRoomsService;
import com.ruoyi.guestHotel.service.IStarhotelsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.ArrayList;
import java.util.List;


@RestController
@RequestMapping("/guest/starhotels")
public class StarhotelRoomsController extends BaseController {
    @Autowired
    private IStarhotelRoomsService starhotelRoomsService;
    @Autowired
    private IStarhotelsService starhotelsService;

    /**
     * 查询星级酒店房间列表
     */

    @GetMapping("/details/{id}")
    public List<Object> list(@PathVariable("id") Long id)
    {
        startPage();
        List<Object> lst=new ArrayList<>();
        List<StarhotelRooms> list = starhotelRoomsService.selectStarhotelRoomsList(id);
        Starhotels sh= starhotelsService.selectStarhotelsById(id);

        List<StarhotelReviews> list_reviews= starhotelRoomsService.selectStarhotelReviewsList(id);
        List<StarhotelReviewsVO> reviewsVOList=new ArrayList<>();
        list_reviews.forEach(review ->{
            StarhotelReviewsVO starhotelReviewsVO=new StarhotelReviewsVO();
            starhotelReviewsVO.setContent(review.getContent());
            String guestName=starhotelRoomsService.selectUserInfoById(review.getGuest_id()).getUser_name();
            starhotelReviewsVO.setGuest_name(guestName);
            starhotelReviewsVO.setRating(review.getRating());
            starhotelReviewsVO.setReview_date(review.getReview_date());
            String avatar=starhotelRoomsService.selectUserInfoById(review.getGuest_id()).getAvatar();
            starhotelReviewsVO.setAvatar(avatar);
            String roomName=starhotelRoomsService.selectStarhotelRoomsById(review.getRoom_type_id()).getName();
            starhotelReviewsVO.setRoom_type_name(roomName);
            reviewsVOList.add(starhotelReviewsVO);
        });
        lst.add(list);
        lst.add(sh);
        lst.add(reviewsVOList);
        return lst;
    }
    /**
     * 新增星级酒店预订信息
     */
    @PostMapping("/details/{id}")
    public AjaxResult add(@RequestBody StarBookings starBookings)
    {
        return toAjax(starhotelRoomsService.insertStarhotelBookingMsg(starBookings));
    }
}
